from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

from canapea.utils import CustomMetaModel, CustomLogoField, CustomModel, slug_generator


class JobCategory(CustomMetaModel):
    name = models.CharField(max_length=255, verbose_name="Անուն")
    icon = CustomLogoField(verbose_name="Նկար", blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True,
                            null=True, verbose_name="Հղում")
    breadcrumbs_text = models.TextField(blank=True, null=True, verbose_name='Breadcrumb -ի տեքստ')
    breadcrumbs_image = CustomLogoField(blank=True, null=True, verbose_name='Breadcrumb -ի Նկար')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Աշխատանքի բաժին'
        verbose_name_plural = "Աշխատանքի բաժիններ"

    def get_absolute_url(self):
        return reverse('jobs:job_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_generator(title=self.name, model=self.__class__)

        return super().save(*args, **kwargs)


class EmploymentTerm(models.Model):
    title = models.CharField(max_length=255, unique=True,
                             verbose_name="Աշխատանքի պայման")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Աշխատանքի պայման"
        verbose_name_plural = "Աշխատանքի պայմաններ"


class JobType(models.Model):
    title = models.CharField(max_length=255,
                             unique=True,
                             verbose_name="Աշխատանքի տիպը")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Աշխատանքի տիպը"
        verbose_name_plural = "Աշխատանքի տիպը"


class Location(models.Model):
    title = models.CharField(max_length=255,
                             unique=True,
                             verbose_name="Տեղանուն")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Գտնվելու վայրը"
        verbose_name_plural = "Գտնվելու վայրը"


class JobItem(CustomMetaModel):
    category = models.ForeignKey(JobCategory,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 verbose_name="Բաժին")
    name = models.CharField(max_length=255, verbose_name="Հաստիքի անուն")
    slug = models.SlugField(max_length=255, blank=True,
                            null=True, verbose_name="Հղում")
    short_description = RichTextUploadingField(
        verbose_name="Հակիրճ Նկարագիր", blank=True
    )
    large_description = RichTextUploadingField(
        verbose_name="Ամբողջական Նկարագիր"
    )
    employment_term = models.ForeignKey(EmploymentTerm,
                                        on_delete=models.CASCADE,
                                        blank=True, null=True,
                                        verbose_name="Աշխատանքի պայմաններ")
    location = models.ForeignKey(Location,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 verbose_name="Գտնվելու վայրը")
    job_type = models.ForeignKey(JobType,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True,
                                 verbose_name='Աշխատանքի տիպը')
    icon = CustomLogoField(blank=True, null=True)
    dateline = models.DateTimeField(blank=True,
                                    null=True,
                                    verbose_name="Հասանելի է մինչև")
    salary_from = models.IntegerField(blank=True, null=True, verbose_name="Աշխատավարձը սկսած")
    salary_to = models.IntegerField(blank=True, null=True, verbose_name="Աշխատավարձը մինչև")
    is_active = models.BooleanField(default=False, verbose_name="Հաստիքը առկա է")

    def get_absolute_url(self):
        return reverse('jobs:job_details', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Թափուր հաստիք"
        verbose_name_plural = "Թափուր հաստիքներ"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slug_generator(title=self.name, model=self.__class__)

        return super().save(*args, **kwargs)


class SubmittedResumes(CustomModel):
    job = models.ForeignKey(on_delete=models.SET_NULL, null=True, blank=True, to='job.JobItem')
    job_title = models.CharField(max_length=255, null=True, blank=True)
    cv = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'pdf'])])

    def __str__(self):
        return self.job.name

    class Meta:
        verbose_name = 'Ուղարկված CV -ն'
        verbose_name_plural = 'Ուղարկված CV -ներ'

    def save(self, *args, **kwargs):
        if self.job:
            self.job_title = self.job.name

        super().save(*args, **kwargs)


class PhoneNumbers(models.Model):
    phone = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.phone


class CustomResumeForJob(CustomModel):
    GENDER_LIST = [
        (1, 'Արական'),
        (2, 'Իգական'),
        (3, 'Այլ'),
    ]
    job = models.ForeignKey('job.JobItem', on_delete=models.SET_NULL, null=True, blank=True,
                            verbose_name="Հաստիք")
    avatar = models.FileField(blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])], verbose_name="Նկար")
    name = models.CharField(max_length=300, blank=True, null=True, verbose_name="Անուն և ազգանուն")
    gender = models.CharField(choices=GENDER_LIST, blank=True, null=True,
                              max_length=50, verbose_name="Սեռ")
    birthday = models.DateField(blank=True, null=True, verbose_name="Ծննդյան օր")
    email = models.EmailField(blank=True, null=True, verbose_name="Էլ. հասցե")
    address = models.TextField(blank=True, null=True, verbose_name="Հասցե")
    editor1 = models.TextField(blank=True, null=True, verbose_name='Մասնագիտական փորձ')
    editor2 = models.TextField(blank=True, null=True, verbose_name='Կրթություն և դասընթաց')
    editor3 = models.TextField(blank=True, null=True, verbose_name='Մասնագիտական հմտություններ')
    editor4 = models.TextField(blank=True, null=True, verbose_name='Անձնական հմտություններ')
    editor5 = models.TextField(blank=True, null=True, verbose_name='Լեզուներ')
    edito6 = models.TextField(blank=True, null=True,  verbose_name='Այլ տեղեկություններ')
    phone = models.ManyToManyField(PhoneNumbers, blank=True, null=True, verbose_name='Հեռ. համար / համարներ')

    def __str__(self):
        return self.name