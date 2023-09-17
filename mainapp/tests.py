from django.test import TestCase
from rest_framework.test import APITestCase
from users.models import User
from .models import Course, Lesson

class CoursesCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='testpassword132')
        self.course_data = {'title': 'Test Course', 'desc': 'Test Description'}

    def test_create_course(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/courses/', self.course_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 1)
        course = Course.objects.first()
        self.assertEqual(course.title, self.course_data['title'])
        self.assertEqual(course.desc, self.course_data['desc'])

    def test_get_course(self):
        self.client.force_authenticate(user=self.user)
        course = Course.objects.create(title='Test Course', desc='Test Description')
        response = self.client.get(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], course.title)
        self.assertEqual(response_data['desc'], course.desc)

    def test_update_course(self):
        self.client.force_authenticate(user=self.user)
        course = Course.objects.create(title='Test Course', desc='Test Description')
        updated_data = {'title': 'Updated Course', 'desc': 'Updated Description'}
        response = self.client.put(f'/courses/{course.id}/', updated_data)
        self.assertEqual(response.status_code, 200)
        course.refresh_from_db()
        self.assertEqual(course.title, updated_data['title'])
        self.assertEqual(course.desc, updated_data['desc'])

    def test_delete_course(self):
        self.client.force_authenticate(user=self.user)
        course = Course.objects.create(title='Test Course', desc='Test Description')
        response = self.client.delete(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Course.objects.count(), 0)


class LessonsCRUDTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', password='testpassword132')
        self.course = Course.objects.create(title='Test Course', desc='Test Description')
        self.lesson_data = {'title': 'Test Lesson', 'desc': 'Test Description', 'link': 'https://www.youtube.com/'}


    def test_get_lesson(self):
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(title='Test Lesson', desc='Test Description', course=self.course)
        response = self.client.get(f'/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['title'], lesson.title)
        self.assertEqual(response_data['desc'], lesson.desc)


    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/lessons/', self.lesson_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().title, 'Test Lesson')

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(title='Old Title', desc='Old Description', link='https://www.youtube.com/')
        lesson_data = {'title': 'New Title', 'desc': 'New Description', 'link': 'https://www.youtube.com/'}
        response = self.client.put(f'/lessons/{lesson.id}/', lesson_data)
        self.assertEqual(response.status_code, 200)
        lesson.refresh_from_db()
        self.assertEqual(lesson.title, 'New Title')
        self.assertEqual(lesson.desc, 'New Description')


    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(title='Test Lesson', desc='Test Description', link='https://www.youtube.com/')
        response = self.client.delete(f'/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, 204)