from .models import Role, Skill, RoleSkill, UserSkill, Progress, Resource

def calculate_skill_gap(user, target_role=None):
    """
    Centralized skill gap & match percentage business logic according to Section 5.
    Reused across Result page, Dashboard, XML Export, and JSON APIs.
    """
    if not target_role:
        if hasattr(user, 'profile') and user.profile.target_role:
            target_role = user.profile.target_role
        else:
            return None

    role_skills = target_role.role_skills.select_related('skill').prefetch_related('skill__resources').order_by('skill__name')
    user_skills_map = {
        us.skill_id: us.current_level
        for us in UserSkill.objects.filter(user=user)
    }

    # Also map progress records
    progress_map = {
        p.skill_id: p
        for p in Progress.objects.filter(user=user)
    }

    skill_rows = []
    total_required = 0
    total_achieved = 0

    counts = {
        'strong': 0,
        'weak': 0,
        'missing': 0,
        'total': 0,
    }

    for rs in role_skills:
        skill = rs.skill
        req = rs.required_level
        cur = user_skills_map.get(skill.id, 0)
        gap = max(0, req - cur)

        total_required += req
        total_achieved += min(cur, req)

        if cur >= req:
            status = 'Strong'
            badge_class = 'badge-strong'
            counts['strong'] += 1
        elif cur >= 1:
            status = 'Weak'
            badge_class = 'badge-weak'
            counts['weak'] += 1
        else:
            status = 'Missing'
            badge_class = 'badge-missing'
            counts['missing'] += 1

        counts['total'] += 1

        prog = progress_map.get(skill.id)

        skill_rows.append({
            'skill': skill,
            'required_level': req,
            'current_level': cur,
            'gap': gap,
            'status': status,
            'badge_class': badge_class,
            'resources': list(skill.resources.all()),
            'resources_count': skill.resources.count(),
            'progress': prog,
            'progress_status': prog.status if prog else 'Not started',
            'progress_notes': prog.notes if prog else '',
        })

    match_percentage = round((total_achieved / total_required * 100), 1) if total_required > 0 else 0.0

    # Learning completion metrics (for gap skills)
    gap_skills = [s for s in skill_rows if s['gap'] > 0]
    total_gaps = len(gap_skills)
    completed_gaps = sum(1 for s in gap_skills if s['progress_status'] == 'Done')
    in_progress_gaps = sum(1 for s in gap_skills if s['progress_status'] == 'In progress')
    not_started_gaps = total_gaps - completed_gaps - in_progress_gaps
    learning_percentage = round((completed_gaps / total_gaps * 100), 1) if total_gaps > 0 else (100.0 if counts['total'] > 0 else 0.0)

    # Readiness score: match percentage boosted by completed gap skills
    readiness_score = match_percentage

    chart_data = {
        'labels': [s['skill'].name for s in skill_rows],
        'required': [s['required_level'] for s in skill_rows],
        'current': [s['current_level'] for s in skill_rows],
    }

    return {
        'target_role': target_role,
        'skills': skill_rows,
        'gap_skills': gap_skills,
        'total_required': total_required,
        'total_achieved': total_achieved,
        'match_percentage': match_percentage,
        'readiness_score': readiness_score,
        'counts': counts,
        'chart_data': chart_data,
        'learning_progress': {
            'total_gaps': total_gaps,
            'completed': completed_gaps,
            'in_progress': in_progress_gaps,
            'not_started': not_started_gaps,
            'percentage': learning_percentage,
        }
    }
