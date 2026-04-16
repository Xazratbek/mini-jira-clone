from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify
from django.urls import reverse

class RoleChoice(models.TextChoices):
    ADMIN = "admin", "Admin"
    OWNER = "owner", "Owner"
    MANAGER = "manager", "Manager"
    MEMBER = "member", "Member"

class Organization(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="organization/logo/%Y/%m/%d/", null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=30,blank=True)
    email = models.EmailField(max_length=150, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while Organization.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization-detail", kwargs={"pk": self.pk})

    def user_role(self, user):
        if not user or not user.is_authenticated:
            return None
        if self.owner_id == user.id:
            return RoleChoice.OWNER
        membership = self.memberships.filter(user=user, is_active=True).values_list("role", flat=True).first()
        return membership

    def is_member(self, user):
        if not user or not user.is_authenticated:
            return False
        return self.owner_id == user.id or self.memberships.filter(user=user, is_active=True).exists()

    def can_manage(self, user):
        return self.user_role(user) in {
            RoleChoice.OWNER,
            RoleChoice.ADMIN,
            RoleChoice.MANAGER,
        }

    class Meta:
        db_table = 'organization'
        ordering = ["-id"]
        verbose_name = "Organizatsiya"
        verbose_name_plural = "Organizatsiyalar"

class OrganizationMember(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,related_name="memberships")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="organization_memberships")
    role = models.CharField(max_length=15,choices=RoleChoice.choices, default=RoleChoice.MEMBER)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL,related_name="organization_creator")

    def __str__(self):
        return f"Org: {self.organization.name} | User: {self.user.username} | Role: {self.role}"

    class Meta:
        db_table = "organization_members"
        ordering = ["-id"]
        verbose_name = 'Organization Member'
        verbose_name_plural = 'Organizatsiya A\'zolari'
        constraints = [
            models.UniqueConstraint(
                fields=["organization","user"],
                name="unique_organization_user"
            )
        ]


def get_user_organization(user):
    if not user or not user.is_authenticated:
        return None

    owned_org = Organization.objects.filter(owner=user, is_active=True).first()
    if owned_org:
        return owned_org

    membership = (
        OrganizationMember.objects.select_related("organization")
        .filter(user=user, is_active=True, organization__is_active=True)
        .order_by("joined_at")
        .first()
    )
    return membership.organization if membership else None
