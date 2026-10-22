from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json
import xml.etree.ElementTree as ET
from .models import Role, Skill, RoleSkill, Profile, UserSkill, Resource, Progress
from .services import calculate_skill_gap

class SkillBridgeComprehensiveTestCase(TestCase):
    """
    Test suite verifying Section 12 Testing Checklist from SKILLBRIDGE_BUILD.md.
    """

    def setUp(self):
        self.client = Client()

        # Seed sample role, skills, and requirements
        self.role = Role.objects.create(name="Full Stack Developer", description="Web engineer")
        self.s1 = Skill.objects.create(name="Python", category="Backend")
        self.s2 = Skill.objects.create(name="HTML", category="Frontend")
        self.s3 = Skill.objects.create(name="SQL", category="Database")

        self.rs1 = RoleSkill.objects.create(role=self.role, skill=self.s1, required_level=4)
        self.rs2 = RoleSkill.objects.create(role=self.role, skill=self.s2, required_level=3)
        self.rs3 = RoleSkill.objects.create(role=self.role, skill=self.s3, required_level=5)

        self.resource1 = Resource.objects.create(
            skill=self.s1,
            title="Python Tutorial",
            link="https://docs.python.org",
            type="Article"
        )

        # Create primary test user
        self.username = "testuser"
        self.password = "pass12345"
        self.user = User.objects.create_user(username=self.username, email="test@example.com", password=self.password)
        self.profile = Profile.objects.create(user=self.user, college="AISSMS IOIT", year="Third Year", target_role=self.role)

    # 1. Authentication Tests
    def test_registration_valid_and_invalid(self):
        # Valid registration
        r = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'college': 'AISSMS IOIT',
            'year': 'Third Year',
            'password': 'secretpassword',
            'confirm_password': 'secretpassword'
        }, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='newuser').exists())

        self.client.logout()

        # Duplicate username rejected
        r_dup = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'dup@example.com',
            'college': 'AISSMS IOIT',
            'year': 'Third Year',
            'password': 'secretpassword',
            'confirm_password': 'secretpassword'
        })
        self.assertEqual(r_dup.status_code, 200)
        self.assertContains(r_dup, 'This username is already taken. Please choose another.')

        # Password mismatch rejected
        r_mismatch = self.client.post(reverse('register'), {
            'username': 'anotheruser',
            'email': 'mismatch@example.com',
            'college': 'AISSMS IOIT',
            'year': 'Third Year',
            'password': 'secretpassword1',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(r_mismatch.status_code, 200)
        self.assertContains(r_mismatch, 'Passwords do not match.')

    def test_login_invalid_credentials(self):
        r = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword'
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Invalid username or password')

    def test_protected_pages_redirect_when_logged_out(self):
        protected_urls = [
            reverse('dashboard'),
            reverse('assessment'),
            reverse('result'),
            reverse('tracker'),
            reverse('profile'),
            reverse('export_xml'),
            reverse('api_result'),
        ]
        for url in protected_urls:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302, f"Expected redirect on {url}")
            self.assertIn('/login/', r['Location'])

    # 2. Role Selection Tests
    def test_choosing_role_updates_profile(self):
        self.client.login(username=self.username, password=self.password)
        new_role = Role.objects.create(name="Data Analyst", description="Data insights")
        r = self.client.post(reverse('role_select', args=[new_role.id]), follow=True)
        self.assertEqual(r.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.target_role, new_role)

    # 3. Assessment & UserSkill Persistence Tests
    def test_assessment_saving_and_deduplication(self):
        self.client.login(username=self.username, password=self.password)
        post_data = {
            'skill_id': [self.s1.id, self.s2.id],
            f'rating_{self.s1.id}': 3,
            f'rating_{self.s2.id}': 2,
        }
        r = self.client.post(reverse('assessment'), post_data, follow=True)
        self.assertEqual(r.status_code, 200)

        # Check records created
        self.assertEqual(UserSkill.objects.filter(user=self.user, skill=self.s1).count(), 1)
        self.assertEqual(UserSkill.objects.get(user=self.user, skill=self.s1).current_level, 3)

        # Re-submitting updates, does NOT duplicate
        post_data[f'rating_{self.s1.id}'] = 4
        self.client.post(reverse('assessment'), post_data, follow=True)
        self.assertEqual(UserSkill.objects.filter(user=self.user, skill=self.s1).count(), 1)
        self.assertEqual(UserSkill.objects.get(user=self.user, skill=self.s1).current_level, 4)

    # 4. Gap Calculation and Match Percentage Logic
    def test_gap_calculation_all_zeros(self):
        # When no skills are rated, current_level defaults to 0
        data = calculate_skill_gap(self.user, self.role)
        self.assertEqual(data['match_percentage'], 0.0)
        self.assertEqual(data['counts']['missing'], 3)
        self.assertEqual(data['counts']['strong'], 0)
        self.assertEqual(data['counts']['weak'], 0)

    def test_gap_calculation_all_required_level(self):
        # Rate all skills at or above required level
        UserSkill.objects.create(user=self.user, skill=self.s1, current_level=4)
        UserSkill.objects.create(user=self.user, skill=self.s2, current_level=3)
        UserSkill.objects.create(user=self.user, skill=self.s3, current_level=5)

        data = calculate_skill_gap(self.user, self.role)
        self.assertEqual(data['match_percentage'], 100.0)
        self.assertEqual(data['counts']['strong'], 3)
        self.assertEqual(data['counts']['weak'], 0)
        self.assertEqual(data['counts']['missing'], 0)

    def test_gap_calculation_mixed_ratings(self):
        # s1: req 4, cur 2 (min=2, gap=2, weak)
        # s2: req 3, cur 3 (min=3, gap=0, strong)
        # s3: req 5, cur 0 (min=0, gap=5, missing)
        # Total req = 4 + 3 + 5 = 12
        # Total achieved = 2 + 3 + 0 = 5
        # Expected % = (5 / 12) * 100 = 41.7%
        UserSkill.objects.create(user=self.user, skill=self.s1, current_level=2)
        UserSkill.objects.create(user=self.user, skill=self.s2, current_level=3)

        data = calculate_skill_gap(self.user, self.role)
        self.assertEqual(data['total_required'], 12)
        self.assertEqual(data['total_achieved'], 5)
        self.assertEqual(data['match_percentage'], 41.7)
        self.assertEqual(data['counts']['strong'], 1)
        self.assertEqual(data['counts']['weak'], 1)
        self.assertEqual(data['counts']['missing'], 1)

    # 5. Tracker & Progress Persistence Tests
    def test_tracker_status_and_notes_persist(self):
        self.client.login(username=self.username, password=self.password)
        UserSkill.objects.create(user=self.user, skill=self.s1, current_level=2)

        notes_text = "Mastered decorators, generator functions, and unit tests"
        r = self.client.post(reverse('tracker'), {
            'skill_id': self.s1.id,
            'status': 'Done',
            'notes': notes_text
        }, follow=True)
        self.assertEqual(r.status_code, 200)

        prog = Progress.objects.get(user=self.user, skill=self.s1)
        self.assertEqual(prog.status, 'Done')
        self.assertEqual(prog.notes, notes_text)

        # Reload tracker page
        r_reload = self.client.get(reverse('tracker'))
        self.assertContains(r_reload, notes_text)

    # 6. XML Export & JSON Endpoint Tests
    def test_xml_export_well_formed(self):
        self.client.login(username=self.username, password=self.password)
        UserSkill.objects.create(user=self.user, skill=self.s1, current_level=4)

        r = self.client.get(reverse('export_xml'))
        self.assertEqual(r.status_code, 200)
        self.assertIn('application/xml', r['Content-Type'])

        # Verify XML is well-formed
        root = ET.fromstring(r.content)
        self.assertEqual(root.tag, 'skillReport')
        self.assertEqual(root.find('metadata/studentUsername').text, self.username)
        self.assertEqual(root.find('metadata/targetRole').text, self.role.name)

    def test_json_endpoints_return_data(self):
        self.client.login(username=self.username, password=self.password)
        UserSkill.objects.create(user=self.user, skill=self.s1, current_level=4)

        r_skills = self.client.get(reverse('api_skills'))
        self.assertEqual(r_skills.status_code, 200)
        d_skills = json.loads(r_skills.content)
        self.assertEqual(d_skills['status'], 'success')
        self.assertEqual(d_skills['user'], self.username)

        r_result = self.client.get(reverse('api_result'))
        self.assertEqual(r_result.status_code, 200)
        d_result = json.loads(r_result.content)
        self.assertEqual(d_result['status'], 'success')
        self.assertEqual(d_result['target_role']['name'], self.role.name)
        self.assertIn('chart_data', d_result)
