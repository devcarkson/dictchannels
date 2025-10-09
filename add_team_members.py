#!/usr/bin/env python
"""
Script to add sample team members to the database.
Run this script to populate the team page with sample data.
"""

import os
import sys
import django

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictchannel.settings')
django.setup()

from pages.models import TeamMember

def add_sample_team_members():
    """Add sample team members to the database."""

    team_members_data = [
        {
            'name': 'John Adebayo',
            'designation': 'CEO & Founder',
            'bio': 'Over 15 years of experience in IT training and software development leadership.',
            'display_order': 1,
        },
        {
            'name': 'Sarah Johnson',
            'designation': 'Lead Instructor',
            'bio': 'Certified instructor with expertise in Python, Java, and web development technologies.',
            'display_order': 2,
        },
        {
            'name': 'Michael Chen',
            'designation': 'Software Developer',
            'bio': 'Full-stack developer specializing in modern web technologies and mobile applications.',
            'display_order': 3,
        },
        {
            'name': 'Grace Okafor',
            'designation': 'Data Science Specialist',
            'bio': 'Expert in machine learning, AI, and big data analytics with industry experience.',
            'display_order': 4,
        },
        {
            'name': 'David Williams',
            'designation': 'Cybersecurity Expert',
            'bio': 'Certified cybersecurity professional with experience in network security and ethical hacking.',
            'display_order': 5,
        },
        {
            'name': 'Amara Nwosu',
            'designation': 'UI/UX Designer',
            'bio': 'Creative designer focused on user experience and modern interface design principles.',
            'display_order': 6,
        },
    ]

    for member_data in team_members_data:
        # Check if member already exists
        if not TeamMember.objects.filter(name=member_data['name']).exists():
            member = TeamMember.objects.create(**member_data)
            print(f"Created team member: {member.name}")
        else:
            print(f"Team member already exists: {member_data['name']}")

    print("Sample team members added successfully!")

if __name__ == '__main__':
    add_sample_team_members()