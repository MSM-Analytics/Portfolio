import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

import { Curriculum } from '../../models/curriculum.model';

(pdfMake as any).vfs = (pdfFonts as any)['vfs'];

export async function generateCvPdf(
  data: Curriculum,
  tipo: 'programador' | 'analista'
): Promise<void> {

  try {
    if (data.personalInfo.photo?.startsWith('assets')) {
      data.personalInfo.photo = await imageToBase64(data.personalInfo.photo);
    }
  } catch (err) {
    console.warn('Erro ao carregar foto do currículo', err);
    data.personalInfo.photo = undefined;
  }

  const docDefinition: any = {
    pageSize: 'A4',
    pageMargins: [40, 120, 40, 50],

    header: buildHeader(data),

    content: [
      buildSummary(data),
      buildExperience(data),
      buildEducation(data),
      buildSkills(data)
    ],

    styles: {
      headerName: {
        fontSize: 20,
        bold: true,
        color: '#1f2937',
        margin: [0, 0, 0, 4]
      },
      headerTitle: {
        fontSize: 11,
        color: '#4f46e5',
        bold: true
      },
      headerContact: {
        fontSize: 9,
        color: '#374151'
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

  const fileName =
    tipo === 'programador'
      ? 'CV_DEV_Rodrigo.pdf'
      : 'CV_AD_Rodrigo.pdf';

  pdfMake.createPdf(docDefinition).download(fileName);
}

/* =======================
   Calcular Idade
======================= */
function calculateAge(date: string): number {
  const birth = new Date(date);
  const today = new Date();

  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();

  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
    age--;
  }

  return age;
}

/* ===============================
   Converter imagem em circular
=============================== */
export function imageToBase64(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';

    img.onload = () => {
      const size = Math.min(img.width, img.height);
      const canvas = document.createElement('canvas');
      canvas.width = size;
      canvas.height = size;

      const ctx = canvas.getContext('2d')!;
      ctx.beginPath();
      ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();

      const sx = (img.width - size) / 2;
      const sy = (img.height - size) / 2;

      ctx.drawImage(img, sx, sy, size, size, 0, 0, size, size);

      resolve(canvas.toDataURL('image/png'));
    };

    img.onerror = reject;
    img.src = url;
  });
}

/* =======================
   HEADER PREMIUM
======================= */
function buildHeader(data: Curriculum) {
  const info = data.personalInfo;
  const age = info.birthDate ? calculateAge(info.birthDate) : null;

  return {
    margin: [0, 0, 0, 18],
    stack: [
      {
        columns: [
          // LADO ESQUERDO
          {
            width: '*',
            columns: [
              info.photo
                ? {
                  image: info.photo,
                  width: 80,
                  height: 80,
                  margin: [0, 0, 12, 0]
                }
                : {},

              {
                width: '*',
                stack: [
                  { text: info.name, style: 'headerName', margin: [20, 0, 0, 0] },
                  {
                    text: [
                      info.title || '',
                      info.maritalStatus ? ` | ${info.maritalStatus}` : '',
                      age ? ` | ${age} anos` : ''
                    ].join(''),
                    style: 'headerTitle',
                    margin: [20, 2, 0, 6]
                  },
                  {
                    text: `${info.email} | ${info.phone}`,
                    style: 'headerContact',
                    margin: [20, 0, 0, 0]
                  },
                  info.address
                    ? {
                      text: info.address,
                      style: 'headerContact',
                      margin: [20, 2, 0, 0]
                    }
                    : {}
                ]
              }
            ]
          },

          // LADO DIREITO — QR CODES
          {
            width: 'auto',
            columns: [
              info.linkedin
                ? {
                  width: 70,
                  stack: [
                    {
                      text: 'LinkedIn',
                      link: info.linkedin,
                      fontSize: 8,
                      bold: true,
                      color: '#4f46e5',
                      alignment: 'center',
                      margin: [0, 0, 0, 4]
                    },
                    {
                      qr: info.linkedin,
                      fit: 60,
                      alignment: 'center',
                    }
                  ]
                }
                : {},

              info.github
                ? {
                  width: 70,
                  margin: [8, 0, 0, 0],
                  stack: [
                    {
                      text: 'GitHub',
                      link: info.github,
                      fontSize: 8,
                      bold: true,
                      color: '#111827',
                      alignment: 'center',
                      margin: [0, 0, 0, 4]
                    },
                    {
                      qr: info.github,
                      fit: 60,
                      alignment: 'center',
                    }
                  ]
                }
                : {}
            ]
          }
        ]
      },

      // DIVISOR PREMIUM
      {
        canvas: [
          {
            type: 'line',
            x1: 0,
            y1: 0,
            x2: 530,
            y2: 0,
            lineWidth: 1,
            lineColor: '#4f46e5'
          }
        ],
        margin: [0, 12, 0, 12]
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

      ...(data.experiences ?? []).map(exp => ({
        unbreakable: true,
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

      ...(data.education ?? []).map(edu => ({
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
          { width: '50%', stack: buildSkillColumn(data.skills ?? [], 0) },
          { width: '50%', stack: buildSkillColumn(data.skills ?? [], 1) }
        ],
        columnGap: 20
      }
    ]
  };
}

/* =======================
   SKILL COLUMN
======================= */
function buildSkillColumn(skills: any[], columnIndex: number) {
  return skills
    .filter((_, index) => index % 2 === columnIndex)
    .map(skill => ({
      unbreakable: true,
      margin: [0, 0, 0, 10],
      stack: [
        { text: skill.category, style: 'experienceCompany' },
        { text: skill.items.join(' • '), style: 'paragraph' }
      ]
    }));
}