from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Course_Taken


class ApplicationTests(TestCase):
    def test_pages(self):
        for name in ['index', 'add_student', 'add_course', 'report_student']:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_student_course_and_report_workflow(self):
        self.assertRedirects(self.client.post(reverse('add_student'), {
            'Student_id': 123, 'Student_name': 'Demo Student', 'gpa': 0,
        }), reverse('index'))
        for course_id, credits, grade in [(101, 3, 90), (102, 1, 70)]:
            self.assertRedirects(self.client.post(reverse('add_course'), {
                'Student_id': 123, 'Course_id': course_id, 'Semester': 'Fall',
                'Number_of_credits': credits, 'Grade': grade,
            }), reverse('index'))
        self.assertEqual(Student.objects.get(pk=123).gpa, 85)
        report = self.client.post(reverse('report_student'), {'Student_id': 123})
        self.assertContains(report, 'Demo Student')
        self.assertContains(report, '85')

    def test_missing_student_report_is_validation_error(self):
        response = self.client.post(reverse('report_student'), {'Student_id': 999})
        self.assertContains(response, 'No student with this ID was found.')

    def test_zero_credits_rejected(self):
        Student.objects.create(Student_id=123, Student_name='Demo')
        response = self.client.post(reverse('add_course'), {
            'Student_id': 123, 'Course_id': 101, 'Semester': 'Fall',
            'Number_of_credits': 0, 'Grade': 90,
        })
        self.assertContains(response, 'Credits must be greater than zero.')
        self.assertFalse(Course_Taken.objects.exists())


class DeleteTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(Student_id=90001, Student_name='Test')
        self.course = Course_Taken.objects.create(Student_id=self.student, Course_id=1, Semester='Fall', Number_of_credits=3, Grade=80)

    def test_get_cannot_delete(self):
        for route, pk in [('delete_student', self.student.pk), ('delete_course', self.course.pk)]:
            self.assertEqual(self.client.get(reverse(route, args=[pk])).status_code, 405)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())
        self.assertTrue(Course_Taken.objects.filter(pk=self.course.pk).exists())

    def test_student_delete_cascades(self):
        response = self.client.post(reverse('delete_student', args=[self.student.pk]))
        self.assertRedirects(response, reverse('add_student'))
        self.assertFalse(Student.objects.exists())
        self.assertFalse(Course_Taken.objects.exists())

    def test_course_delete_updates_gpa(self):
        other = Course_Taken.objects.create(Student_id=self.student, Course_id=2, Semester='Fall', Number_of_credits=3, Grade=60)
        self.assertRedirects(self.client.post(reverse('delete_course', args=[self.course.pk])), reverse('add_course'))
        self.student.refresh_from_db()
        self.assertEqual(self.student.gpa, 60)
        self.client.post(reverse('delete_course', args=[other.pk]))
        self.student.refresh_from_db()
        self.assertEqual(self.student.gpa, 0)

    def test_csrf_required(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse('delete_student', args=[self.student.pk])).status_code, 403)
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

    def test_delete_controls_render(self):
        self.assertContains(self.client.get(reverse('add_student')), 'Delete student 90001')
        self.assertContains(self.client.get(reverse('add_course')), 'Delete course 1')
