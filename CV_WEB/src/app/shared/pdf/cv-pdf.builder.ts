import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

import { Curriculum } from '../../models/curriculum.model';

(pdfMake as any).vfs = (pdfFonts as any)['vfs'];

export function generateCvPdf(data: Curriculum): void {
    const docDefinition: any = {
        pageSize: 'A4',
        pageMargins: [40, 50, 40, 50],

        content: [
            buildHeader(data),
            buildSummary(data),
            buildExperience(data),
            buildEducation(data),
            buildSkills(data)
        ],

        styles: {
            headerName: {
                fontSize: 20,
                bold: true,
                color: '#111827',
                margin: [0, 0, 0, 4]
            },
            headerTitle: {
                fontSize: 12,
                color: '#374151',
                margin: [0, 0, 0, 10]
            },
            headerContact: {
                fontSize: 9,
                color: '#4B5563',
                margin: [0, 0, 0, 20]
            },
            sectionTitle: {
                fontSize: 14,
                bold: true,
                color: '#1F2937',
                margin: [0, 20, 0, 8]
            },
            paragraph: {
                fontSize: 10,
                color: '#111827',
                lineHeight: 1.4
            },
            experienceRole: {
                fontSize: 11,
                bold: true,
                color: '#111827'
            },
            experienceCompany: {
                fontSize: 10,
                bold: true,
                color: '#2563EB'
            },
            experienceMeta: {
                fontSize: 9,
                color: '#6B7280',
                margin: [0, 2, 0, 4]
            },
            bullet: {
                fontSize: 10,
                margin: [0, 0, 0, 2]
            }

        }
    };

    pdfMake.createPdf(docDefinition).download('Rodrigo_Matos_CV.pdf');
}

/* =======================
   HEADER
======================= */
function buildHeader(data: Curriculum) {
  const info = data.personalInfo;

  return {
    margin: [0, 0, 0, 20],
    stack: [
      {
        columns: [
          {
            width: '*',
            stack: [
              { text: info.name, style: 'headerName' },
              { text: info.title, style: 'headerTitle' }
            ]
          },
          {
            width: 'auto',
            alignment: 'right',
            stack: [
              { text: info.location, style: 'headerContact' },
              { text: info.email, style: 'headerContact' },
              info.linkedin ? { text: info.linkedin, style: 'headerContact' } : {}
            ]
          }
        ]
      }
    ]
  };
}

/* =======================
   SUMMARY
======================= */
function buildSummary(data: Curriculum) {
    return {
        stack: [
            { text: 'Resumo Profissional', style: 'sectionTitle' },
            { text: data.summary, style: 'paragraph' }
        ]
    };
}

/* =======================
   EXPERIENCE
======================= */
function buildExperience(data: Curriculum) {
  return {
    stack: [
      { text: 'Experiência Profissional', style: 'sectionTitle' },

      ...data.experiences.map(exp => ({
        unbreakable: true, // 🔥 impede corte no meio
        margin: [0, 0, 0, 14],
        stack: [
          { text: exp.position, style: 'experienceRole' },
          { text: exp.company, style: 'experienceCompany' },
          {
            text: `${exp.location} • ${exp.startDate} - ${exp.current ? 'Atual' : exp.endDate}`,
            style: 'experienceMeta'
          },
          {
            ul: exp.description.map(item => ({
              text: item,
              style: 'bullet'
            }))
          }
        ]
      }))
    ]
  };
}

/* =======================
   EDUCATION
======================= */
function buildEducation(data: Curriculum) {
  return {
    stack: [
      { text: 'Formação Acadêmica', style: 'sectionTitle' },

      ...data.education.map(edu => ({
        unbreakable: true,
        margin: [0, 0, 0, 14],
        stack: [
          { text: edu.degree, style: 'experienceRole' },
          { text: edu.institution, style: 'experienceCompany' },
          {
            text: `${edu.location} • ${edu.startDate} - ${edu.endDate}`,
            style: 'experienceMeta'
          },
          {
            ul: edu.description.map(item => ({
              text: item,
              style: 'bullet'
            }))
          }
        ]
      }))
    ]
  };
}
/* =======================
   SKILLS
======================= */
function buildSkills(data: Curriculum) {
  return {
    stack: [
      { text: 'Habilidades', style: 'sectionTitle' },

      {
        columns: [
          {
            width: '50%',
            stack: buildSkillColumn(data.skills, 0)
          },
          {
            width: '50%',
            stack: buildSkillColumn(data.skills, 1)
          }
        ],
        columnGap: 20
      }
    ]
  };
}

/* =======================
   SKILL COLUMN HELPER
======================= */
function buildSkillColumn(skills: any[], columnIndex: number) {
  return skills
    .filter((_, index) => index % 2 === columnIndex)
    .map(skill => ({
      unbreakable: true,
      margin: [0, 0, 0, 10],
      stack: [
        { text: skill.category, style: 'experienceCompany' },
        {
          text: skill.items.join(' • '),
          style: 'paragraph'
        }
      ]
    }));
}

