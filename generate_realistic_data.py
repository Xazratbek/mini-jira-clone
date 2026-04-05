"""
Realistic data generator for Mini Jira Clone
Generates 100 users, projects, tasks, comments with realistic relationships.
Activity logs are auto-generated via signals.
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from faker import Faker
from accounts.models import CustomUser
from projects.models import Project
from tasks.models import Task, TaskStatusChoice, TaskPriorityChoice
from comments.models import Comment

# Initialize Faker with multiple locales for realistic data
fake = Faker(['en_US', 'fr_FR', 'de_DE', 'es_ES'])
Faker.seed(42)
random.seed(42)

# Sample data for realistic content
PROJECT_DESCRIPTIONS = [
    "E-commerce platform development with modern UI/UX",
    "Mobile app for real-time collaboration",
    "Cloud infrastructure automation tools",
    "Social media analytics dashboard",
    "AI-powered customer support system",
    "Data visualization and reporting platform",
    "Microservices architecture implementation",
    "Cybersecurity monitoring solution",
    "IoT device management system",
    "Machine learning model deployment pipeline",
    "Blockchain-based supply chain tracking",
    "Video streaming platform optimization",
    "Database migration and optimization",
    "API gateway and security implementation",
    "DevOps automation and CI/CD pipeline",
]

TASK_TITLES = [
    "Implement user authentication",
    "Design database schema",
    "Create API endpoints",
    "Build frontend components",
    "Write unit tests",
    "Setup CI/CD pipeline",
    "Deploy to production",
    "Fix critical bugs",
    "Optimize database queries",
    "Create documentation",
    "Implement caching strategy",
    "Setup monitoring and logging",
    "Code review and refactoring",
    "Security audit and fixes",
    "Performance optimization",
    "Implement new feature",
    "Fix integration issues",
    "Setup development environment",
    "Write API documentation",
    "Create user guide",
]

COMMENT_TEMPLATES = [
    "Great work! This looks solid.",
    "I have some concerns about the implementation. Let's discuss.",
    "Can you add more test coverage for this?",
    "The performance looks good on my machine.",
    "Nice implementation! Ready to merge.",
    "I found a potential bug here. Can you check?",
    "This needs more documentation.",
    "Looks good! Just minor tweaks needed.",
    "Can we optimize this further?",
    "Excellent work on this feature!",
    "Let's pair on this to understand better.",
    "The code quality looks excellent.",
    "I think we should refactor this part.",
    "This approach seems risky. Any alternatives?",
    "Great attention to detail here!",
]




def create_users(count=100):
    """Create realistic users with email and names"""
    print(f"Creating {count} users...")
    users = []

    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Create unique username
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(100, 999)}"
        email = fake.unique.email()

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password='Test@1234',
        )
        users.append(user)

        if (i + 1) % 20 == 0:
            print(f"  ✓ Created {i + 1} users")

    print(f"✓ All {count} users created successfully!\n")
    return users


def create_projects(users, count=20):
    """Create projects with owners and members"""
    print(f"Creating {count} projects...")
    projects = []

    for i in range(count):
        owner = random.choice(users)

        project = Project.objects.create(
            name=fake.bs().title()[:150],
            description=random.choice(PROJECT_DESCRIPTIONS),
            owner=owner,
        )

        # Add random members (3-15 members per project)
        num_members = random.randint(3, 15)
        members = random.sample(users, min(num_members, len(users)))
        project.members.set(members)

        projects.append(project)

        if (i + 1) % 5 == 0:
            print(f"  ✓ Created {i + 1} projects")

    print(f"✓ All {count} projects created successfully!\n")
    return projects


def create_tasks(users, projects, count=250):
    """Create tasks with assignments and relationships"""
    print(f"Creating {count} tasks...")
    tasks = []

    for i in range(count):
        project = random.choice(projects)
        created_by = random.choice(project.members.all()) if project.members.exists() else random.choice(users)
        assigned_to = random.choice(project.members.all()) if project.members.exists() else random.choice(users)

        # Generate due date (between today and 90 days from now)
        days_offset = random.randint(1, 90)
        due_date = timezone.now().date() + timedelta(days=days_offset)

        task = Task.objects.create(
            title=random.choice(TASK_TITLES),
            description=fake.paragraph(nb_sentences=random.randint(2, 5)),
            project=project,
            assigned_to=assigned_to,
            created_by=created_by,
            status=random.choice([choice[0] for choice in TaskStatusChoice.choices]),
            priority=random.choice([choice[0] for choice in TaskPriorityChoice.choices]),
            due_date=due_date,
        )
        tasks.append(task)

        if (i + 1) % 50 == 0:
            print(f"  ✓ Created {i + 1} tasks")

    print(f"✓ All {count} tasks created successfully!\n")
    return tasks


def create_comments(users, tasks, count=400):
    """Create comments on tasks"""
    print(f"Creating {count} comments...")

    for i in range(count):
        task = random.choice(tasks)
        author = random.choice(users)

        Comment.objects.create(
            task=task,
            author=author,
            content=random.choice(COMMENT_TEMPLATES),
        )

        if (i + 1) % 80 == 0:
            print(f"  ✓ Created {i + 1} comments")

    print(f"✓ All {count} comments created successfully!\n")


def clear_existing_data():
    """Clear all existing data (use with caution)"""
    print("Clearing existing data...")
    Comment.objects.all().delete()
    Task.objects.all().delete()
    Project.objects.all().delete()
    CustomUser.objects.all().delete()
    print("✓ All data cleared!\n")


def main():
    """Main function to orchestrate data generation"""
    print("=" * 60)
    print("Mini Jira Clone - Realistic Data Generator")
    print("=" * 60)
    print()

    # Clear existing data automatically
    clear_existing_data()

    try:
        # Generate data
        users = create_users(count=100)
        projects = create_projects(users, count=20)
        tasks = create_tasks(users, projects, count=250)
        create_comments(users, tasks, count=400)

        # Print summary
        print("=" * 60)
        print("Data Generation Summary")
        print("=" * 60)
        print(f"✓ Users created:           {CustomUser.objects.count()}")
        print(f"✓ Projects created:        {Project.objects.count()}")
        print(f"✓ Tasks created:           {Task.objects.count()}")
        print(f"✓ Comments created:        {Comment.objects.count()}")
        print(f"✓ Activity logs created:   Auto-generated via signals")
        print("=" * 60)
        print()
        print("✓ Data generation completed successfully!")

    except Exception as e:
        print(f"\n✗ Error during data generation: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
