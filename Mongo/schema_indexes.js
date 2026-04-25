/*
  Plataforma de Educación en Línea - MongoDB
  Este archivo define colecciones, índices, ejemplos de documentos
  y pipelines conceptuales de agregación.
*/

use("online_learning_platform");

// =====================================================
// 1) Creación de colecciones
// =====================================================
db.createCollection("users");
db.createCollection("courses");
db.createCollection("enrollments");
db.createCollection("quizzes");
db.createCollection("certificates");
db.createCollection("course_reviews");

// =====================================================
// 2) Índices
// =====================================================

// users (M05 + M06)
db.users.createIndex({ user_id: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });

// courses (M01 + M02)
db.courses.createIndex({ course_id: 1 }, { unique: true });
db.courses.createIndex({ category: 1 });
db.courses.createIndex({ instructor_id: 1 });
db.courses.createIndex({ title: "text", description: "text" });
db.courses.createIndex({ category: 1, language: 1 });

// enrollments (M03 + M09)
db.enrollments.createIndex({ user_id: 1, course_id: 1 });
db.enrollments.createIndex({ user_id: 1, status: 1 });

// quizzes (M07)
db.quizzes.createIndex({ quiz_id: 1 }, { unique: true });
db.quizzes.createIndex({ course_id: 1 });

// certificates (M08)
db.certificates.createIndex({ user_id: 1 });

// course_reviews (M10)
db.course_reviews.createIndex({ course_id: 1 });
db.course_reviews.createIndex({ user_id: 1 });
db.course_reviews.createIndex({ course_id: 1, rating: 1 });

// =====================================================
// 3) Ejemplos de documentos (comentados)
// =====================================================

/* users
{
  user_id: "U001",
  username: "manuel_lp",
  email: "manuel@example.com",
  hashed_password: "<hash>",
  role: "student",
  created_at: ISODate("2026-03-01T10:00:00Z"),
  profile: {
    full_name: "Manuel Alfonso Lopez Ponce De Leon",
    bio: "Estudiante interesado en datos",
    interests: ["NoSQL", "Backend"],
    preferred_language: "es",
    learning_goals: ["Aprobar el curso", "Construir portafolio"],
    updated_at: ISODate("2026-03-10T12:00:00Z")
  }
}
*/

/* courses
{
  course_id: "C001",
  title: "Introducción a MongoDB",
  description: "Curso base de modelado documental.",
  category: "Databases",
  language: "es",
  instructor_id: "M001",
  is_published: true,
  created_at: ISODate("2026-02-20T09:00:00Z"),
  lessons: [
    {
      lesson_id: "L001",
      title: "Documentos y colecciones",
      attachments: [
        {
          attachment_id: "A001",
          title: "Diapositivas",
          type: "pdf",
          url: "https://example.edu/materiales/mongo-intro.pdf",
          uploaded_at: ISODate("2026-02-21T11:00:00Z")
        }
      ]
    }
  ]
}
*/

/* enrollments
{
  enrollment_id: "E001",
  user_id: "U001",
  course_id: "C001",
  course_title: "Introducción a MongoDB",
  completed_lessons: ["L001"],
  progress_percentage: 25,
  status: "active",
  last_accessed_at: ISODate("2026-04-20T08:45:00Z")
}
*/

/* quizzes
{
  quiz_id: "Q001",
  course_id: "C001",
  title: "Quiz 1 - Fundamentos",
  passing_score: 70,
  max_attempts: 3,
  questions: [
    { question_id: "Q1", prompt: "¿Qué es un documento?", type: "multiple_choice" }
  ]
}
*/

/* certificates
{
  certificate_id: "CERT001",
  user_id: "U001",
  course_id: "C001",
  course_title: "Introducción a MongoDB",
  issue_date: ISODate("2026-04-15T00:00:00Z"),
  verification_code: "VER-ABC-001"
}
*/

/* course_reviews
{
  review_id: "R001",
  course_id: "C001",
  user_id: "U001",
  rating: 5,
  comment: "Muy claro y bien estructurado.",
  created_at: ISODate("2026-04-18T18:30:00Z"),
  status: "published"
}
*/

// =====================================================
// 4) Pipelines de agregación conceptuales
// =====================================================

// Pipeline 1: Promedio de rating por curso (M10)
const pipeline_avg_rating_by_course = [
  { $match: { status: "published" } },
  {
    $group: {
      _id: "$course_id",
      avg_rating: { $avg: "$rating" },
      total_reviews: { $sum: 1 }
    }
  },
  { $sort: { avg_rating: -1, total_reviews: -1 } }
];

// Pipeline 2: Resumen de progreso por usuario (M03/M09)
const pipeline_progress_summary_by_user = [
  {
    $group: {
      _id: "$user_id",
      courses_enrolled: { $sum: 1 },
      avg_progress: { $avg: "$progress_percentage" },
      active_courses: {
        $sum: { $cond: [{ $eq: ["$status", "active"] }, 1, 0] }
      }
    }
  },
  { $sort: { avg_progress: -1 } }
];

// Pipeline 3: Cursos más populares por categoría (M02/M09)
// Opción A: con $lookup hacia courses
const pipeline_popular_courses_by_category_lookup = [
  {
    $group: {
      _id: "$course_id",
      total_enrollments: { $sum: 1 }
    }
  },
  {
    $lookup: {
      from: "courses",
      localField: "_id",
      foreignField: "course_id",
      as: "course"
    }
  },
  { $unwind: "$course" },
  {
    $group: {
      _id: "$course.category",
      total_enrollments: { $sum: "$total_enrollments" },
      courses: {
        $push: {
          course_id: "$_id",
          title: "$course.title",
          enrollments: "$total_enrollments"
        }
      }
    }
  },
  { $sort: { total_enrollments: -1 } }
];

// Opción B (alternativa de rendimiento): duplicar `course_title` y `category` en enrollments
// para evitar $lookup en consultas de alta frecuencia.
