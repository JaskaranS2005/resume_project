import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  ArrowRight,
  BarChart3,
  BookOpen,
  Brain,
  Check,
  ChevronDown,
  ClipboardCheck,
  Eye,
  FileText,
  FileSearch,
  Gauge,
  GraduationCap,
  Layers,
  Network,
  Sparkles,
  Target,
  TrendingDown,
  TrendingUp,
  Upload,
} from "lucide-react";

const ROLE_TEMPLATES = [
  {
    name: "Frontend Developer",
    level: "Experienced",
    summary: "React UI engineering with production API integration and performance work.",
    skills: ["React", "JavaScript", "TypeScript", "Redux", "REST APIs", "Responsive UI"],
    text: `Role: Frontend Developer
Experience: 1-4 years or equivalent project experience.

We are looking for a frontend developer who can build responsive, accessible, and maintainable web interfaces. The candidate should be comfortable working with React, JavaScript, TypeScript, component-based architecture, state management, API integration, and browser performance.

Required skills:
- React, JavaScript, HTML, CSS, responsive layouts, and reusable components.
- State management with Redux, Context API, Zustand, or similar tools.
- REST API integration, async data loading, form handling, validation, and error states.
- Git, debugging, browser dev tools, and basic testing.
- Understanding of accessibility, performance optimization, and clean UI implementation.

Responsibilities:
- Build feature-complete UI screens from product or design requirements.
- Connect frontend flows with backend APIs.
- Improve page performance, loading states, and cross-device behavior.
- Collaborate with backend developers, designers, and product stakeholders.
- Write clear code, document decisions, and participate in code reviews.

Good resume signals:
- React projects with real data, authentication, dashboards, forms, or API usage.
- Metrics such as improved load time, reduced bugs, or shipped production features.
- Evidence of component reuse, state management, and responsive design.`,
  },
  {
    name: "Frontend Developer Intern",
    level: "Intern",
    summary: "Entry-level React internship focused on UI screens, components, and API basics.",
    skills: ["HTML", "CSS", "JavaScript", "React", "Git", "API basics"],
    text: `Role: Frontend Developer Intern
Experience: Internship, fresher, student, bootcamp graduate, or portfolio-based candidate.

We are looking for a frontend intern who understands the basics of web development and wants to grow by building real product screens. The candidate should know HTML, CSS, JavaScript, React fundamentals, Git basics, and how to consume simple APIs.

Required skills:
- HTML semantic structure, CSS layouts, Flexbox, Grid, and responsive design basics.
- JavaScript fundamentals: arrays, objects, functions, DOM concepts, promises, and async/await.
- React basics: components, props, state, hooks, conditional rendering, lists, and forms.
- Basic API integration using fetch or axios.
- Git, GitHub, debugging, and willingness to learn from code reviews.

Responsibilities:
- Build small UI components and screens from clear requirements.
- Fix UI bugs, spacing issues, responsive problems, and form behavior.
- Connect simple frontend flows to APIs.
- Write readable code and ask clear questions when blocked.
- Document learning and improve implementation after feedback.

Good resume signals:
- Portfolio projects using React and real API calls.
- Cloned or original UI screens with responsive behavior.
- GitHub links, live demos, internship projects, hackathon work, or coursework.
- Clear learning evidence in JavaScript, React hooks, and component structure.`,
  },
  {
    name: "Backend Developer",
    level: "Experienced",
    summary: "Node.js backend role covering APIs, databases, auth, and service reliability.",
    skills: ["Node.js", "Express", "Databases", "REST APIs", "Authentication", "Testing"],
    text: `Role: Backend Developer
Experience: 1-4 years or equivalent backend project experience.

We are looking for a backend developer who can design, build, and maintain reliable APIs and data-driven services. The candidate should understand server-side development, databases, authentication, API design, validation, testing, and deployment basics.

Required skills:
- Node.js, Express, REST API development, routing, middleware, and error handling.
- SQL or NoSQL databases such as PostgreSQL, MySQL, MongoDB, or Redis.
- Authentication and authorization using JWT, sessions, OAuth, or role-based access.
- Data modeling, query optimization, validation, logging, and API documentation.
- Git, testing, debugging, environment variables, and deployment workflows.

Responsibilities:
- Build secure, maintainable backend APIs.
- Design database schemas and implement CRUD workflows.
- Integrate third-party services and frontend clients.
- Improve performance, reliability, error handling, and observability.
- Review code and collaborate with frontend/product teams.

Good resume signals:
- API projects with authentication, database models, deployed services, and tests.
- Evidence of scalability, security, or performance improvements.
- Clear ownership of backend modules, integrations, or production fixes.`,
  },
  {
    name: "Backend Developer Intern",
    level: "Intern",
    summary: "Entry-level backend internship for APIs, database CRUD, and auth fundamentals.",
    skills: ["Node.js", "Express", "MongoDB", "SQL basics", "REST APIs", "Git"],
    text: `Role: Backend Developer Intern
Experience: Internship, fresher, student, bootcamp graduate, or project-based candidate.

We are looking for a backend intern who understands programming fundamentals and can learn production backend development through guided tasks. The candidate should know basic Node.js or Python backend concepts, REST APIs, database CRUD, Git, and debugging.

Required skills:
- Programming fundamentals: functions, modules, arrays, objects, promises, and error handling.
- Basic server development with Node.js, Express, Flask, FastAPI, or similar frameworks.
- REST API basics: routes, request/response, status codes, validation, and JSON.
- Database basics with MongoDB, PostgreSQL, MySQL, or SQLite.
- GitHub, Postman or API testing tools, and environment variable usage.

Responsibilities:
- Implement small API endpoints and database operations.
- Fix validation, response formatting, and basic error handling issues.
- Test APIs with sample data and document endpoints.
- Learn authentication basics and contribute to internal backend tasks.
- Communicate blockers clearly and improve code after review.

Good resume signals:
- CRUD API projects, login/signup flows, database-backed apps, or deployed backend demos.
- Postman collections, GitHub repositories, and clean README files.
- Coursework or mini-projects showing database and API understanding.`,
  },
  {
    name: "Data Scientist",
    level: "Experienced",
    summary: "Python analytics and machine learning role with model evaluation and business insight.",
    skills: ["Python", "Pandas", "NumPy", "Scikit-learn", "SQL", "Model evaluation"],
    text: `Role: Data Scientist
Experience: 1-4 years or equivalent analytics and machine learning project experience.

We are looking for a data scientist who can turn messy data into practical insights and reliable models. The candidate should be comfortable with Python, SQL, exploratory analysis, feature engineering, model training, evaluation, visualization, and explaining results to non-technical stakeholders.

Required skills:
- Python, Pandas, NumPy, SQL, data cleaning, feature engineering, and EDA.
- Machine learning with scikit-learn or similar libraries.
- Model evaluation using metrics such as accuracy, precision, recall, F1, ROC-AUC, RMSE, or MAE.
- Visualization with Matplotlib, Seaborn, Plotly, Tableau, or Power BI.
- Experiment tracking, reproducibility, and communication of insights.

Responsibilities:
- Clean data, build analysis notebooks, and identify trends.
- Train, validate, and compare machine learning models.
- Present business recommendations with clear evidence.
- Work with engineering teams to prepare data pipelines or model outputs.
- Monitor model quality and document assumptions.

Good resume signals:
- End-to-end ML projects with real datasets and clear metrics.
- SQL analysis, dashboards, deployed notebooks, or model explanations.
- Evidence of business impact, data storytelling, or measurable improvement.`,
  },
  {
    name: "Data Science Intern",
    level: "Intern",
    summary: "Entry-level data internship for Python, EDA, dashboards, and beginner ML.",
    skills: ["Python", "Pandas", "SQL basics", "EDA", "Visualization", "ML basics"],
    text: `Role: Data Science Intern
Experience: Internship, fresher, student, bootcamp graduate, or portfolio-based candidate.

We are looking for a data science intern who can work with datasets, write Python notebooks, clean data, create visualizations, and learn basic machine learning workflows. The candidate should be comfortable with Python basics, Pandas, SQL basics, charts, and explaining findings.

Required skills:
- Python fundamentals, Pandas, NumPy, Jupyter notebooks, and data cleaning.
- SQL basics: select, filter, join, group by, and aggregation.
- Exploratory data analysis and visualization using Matplotlib, Seaborn, Plotly, or Power BI.
- Basic machine learning concepts: train/test split, classification, regression, and evaluation metrics.
- Clear written explanations of insights and assumptions.

Responsibilities:
- Clean datasets and prepare analysis notebooks.
- Create charts, summaries, and simple dashboards.
- Build beginner ML models under guidance.
- Compare model performance and explain results.
- Document steps so the analysis can be reproduced.

Good resume signals:
- Kaggle, coursework, capstone, or internship analysis projects.
- Notebooks with clean EDA, charts, and conclusions.
- SQL practice, dashboard screenshots, and simple ML metrics.`,
  },
  {
    name: "Full Stack Developer",
    level: "Experienced",
    summary: "MERN-style role covering frontend, backend APIs, databases, and deployment.",
    skills: ["React", "Node.js", "MongoDB", "APIs", "Authentication", "Deployment"],
    text: `Role: Full Stack Developer
Experience: 1-4 years or equivalent full stack project experience.

We are looking for a full stack developer who can own features from frontend screens to backend APIs and database models. The candidate should understand React, Node.js, API integration, database CRUD, authentication, Git workflows, and deployment basics.

Required skills:
- Frontend: React, JavaScript or TypeScript, component design, forms, routing, and responsive UI.
- Backend: Node.js, Express, REST APIs, validation, authentication, and error handling.
- Databases: MongoDB, PostgreSQL, MySQL, or similar data stores.
- Git, environment configuration, testing basics, and deployment.
- Ability to debug across frontend, backend, and API boundaries.

Responsibilities:
- Build complete product features across UI, API, and database layers.
- Implement login, dashboards, forms, CRUD workflows, and integrations.
- Improve code quality, performance, and user experience.
- Collaborate with designers, backend/frontend peers, and product stakeholders.
- Ship features with clear documentation and maintainable structure.

Good resume signals:
- Full stack deployed projects with auth, database, APIs, and frontend UI.
- MERN, Next.js, Django, FastAPI, or similar end-to-end apps.
- Clear project links, GitHub repos, live demos, and measurable outcomes.`,
  },
  {
    name: "Full Stack Developer Intern",
    level: "Intern",
    summary: "Entry-level full stack internship for React screens, simple APIs, and database tasks.",
    skills: ["React basics", "Node.js basics", "CRUD", "MongoDB", "Git", "Deployment basics"],
    text: `Role: Full Stack Developer Intern
Experience: Internship, fresher, student, bootcamp graduate, or portfolio-based candidate.

We are looking for a full stack intern who can learn by building small end-to-end features. The candidate should understand frontend basics, backend API basics, database CRUD, GitHub workflows, and how different parts of a web app connect.

Required skills:
- HTML, CSS, JavaScript, React components, hooks, and forms.
- Basic backend development with Node.js, Express, Flask, FastAPI, or similar.
- REST API basics, JSON, status codes, validation, and Postman testing.
- Database basics with MongoDB, SQL, SQLite, or Firebase.
- Git, GitHub, simple deployment, and clear README documentation.

Responsibilities:
- Build small UI screens and connect them to simple APIs.
- Add database-backed CRUD features under guidance.
- Fix frontend/backend bugs and document changes.
- Test flows manually and report edge cases.
- Learn code structure, reviews, and deployment practices.

Good resume signals:
- Deployed mini apps with frontend, backend, and database.
- Login flow, task manager, e-commerce, dashboard, or student project.
- GitHub repository, screenshots, demo links, and readable documentation.`,
  },
  {
    name: "Machine Learning Engineer Intern",
    level: "Intern",
    summary: "Internship for Python ML projects, model training, evaluation, and simple deployment.",
    skills: ["Python", "Scikit-learn", "Pandas", "Model metrics", "APIs", "ML projects"],
    text: `Role: Machine Learning Engineer Intern
Experience: Internship, fresher, student, or portfolio-based ML candidate.

We are looking for an ML engineering intern who can work with datasets, train baseline models, evaluate results, and learn how models are served inside applications. The candidate should know Python, data preprocessing, basic machine learning algorithms, and model evaluation.

Required skills:
- Python, Pandas, NumPy, scikit-learn, and Jupyter notebooks.
- Data preprocessing, train/test split, feature engineering, and model evaluation.
- Basic algorithms such as linear regression, logistic regression, decision trees, random forest, or clustering.
- Understanding of metrics such as accuracy, F1, precision, recall, RMSE, and MAE.
- Basic API or app integration is a plus.

Responsibilities:
- Prepare datasets and train baseline models.
- Compare model performance and explain tradeoffs.
- Package simple ML workflows for demos or internal tools.
- Document assumptions, experiments, and improvement ideas.
- Learn model serving, monitoring, and reproducibility practices.

Good resume signals:
- ML notebooks with clean preprocessing and metrics.
- Capstone, Kaggle, research, or course projects.
- Simple deployed ML apps using Streamlit, Flask, FastAPI, or similar tools.`,
  },
  {
    name: "QA Automation Intern",
    level: "Intern",
    summary: "Testing internship for manual QA, test cases, bug reports, and automation basics.",
    skills: ["Manual testing", "Test cases", "Bug reports", "Selenium", "Playwright", "API testing"],
    text: `Role: QA Automation Intern
Experience: Internship, fresher, student, or project-based testing candidate.

We are looking for a QA automation intern who can write clear test cases, find bugs, document issues, and learn browser or API automation. The candidate should understand manual testing basics, test scenarios, bug reporting, and entry-level automation tools.

Required skills:
- Manual testing, test case writing, regression testing, and bug reports.
- Basic understanding of web apps, forms, APIs, and browser behavior.
- Exposure to Selenium, Playwright, Cypress, Postman, or similar tools.
- Basic programming in JavaScript, Python, or Java is a plus.
- Clear communication and attention to detail.

Responsibilities:
- Create and execute test cases for web application flows.
- Report bugs with steps, screenshots, expected result, and actual result.
- Help automate repeated test scenarios.
- Validate fixes and maintain simple test documentation.
- Work with developers to reproduce and resolve issues.

Good resume signals:
- Test plans, bug reports, Postman collections, or automation scripts.
- Testing of student projects, internships, hackathon apps, or cloned products.
- Evidence of structured thinking and careful documentation.`,
  },
  {
    name: "DevOps Intern",
    level: "Intern",
    summary: "Cloud and deployment internship for Linux, GitHub Actions, Docker, and CI/CD basics.",
    skills: ["Linux", "Git", "Docker", "CI/CD", "Cloud basics", "Monitoring basics"],
    text: `Role: DevOps Intern
Experience: Internship, fresher, student, or project-based infrastructure candidate.

We are looking for a DevOps intern who can learn deployment workflows, automation, containers, and basic cloud operations. The candidate should understand Linux basics, Git, environment variables, Docker fundamentals, and CI/CD concepts.

Required skills:
- Linux commands, shell basics, Git, GitHub, and environment configuration.
- Docker basics: images, containers, Dockerfile, ports, and volumes.
- CI/CD basics using GitHub Actions, GitLab CI, Jenkins, or similar.
- Basic cloud familiarity with AWS, Azure, GCP, Render, Railway, Vercel, or Netlify.
- Interest in logs, monitoring, deployment reliability, and automation.

Responsibilities:
- Help configure deployments for web applications and APIs.
- Write or update Dockerfiles and simple CI workflows.
- Document setup steps and environment requirements.
- Monitor logs, identify deployment issues, and support fixes.
- Learn infrastructure security and repeatable release practices.

Good resume signals:
- Deployed apps, Dockerized projects, CI/CD workflows, or Linux practice.
- GitHub Actions YAML, cloud deployments, or system setup documentation.
- Clear README files showing setup and deployment steps.`,
  },
  {
    name: "UI UX Design Intern",
    level: "Intern",
    summary: "Design internship for user flows, wireframes, Figma, prototypes, and handoff basics.",
    skills: ["Figma", "Wireframes", "User flows", "Prototypes", "Design systems", "Usability"],
    text: `Role: UI UX Design Intern
Experience: Internship, fresher, student, bootcamp graduate, or portfolio-based design candidate.

We are looking for a UI UX design intern who can support product design through user flows, wireframes, interface mockups, prototypes, and usability improvements. The candidate should be comfortable with Figma, design fundamentals, visual hierarchy, and clear design communication.

Required skills:
- Figma, wireframes, user flows, clickable prototypes, and layout fundamentals.
- Understanding of typography, spacing, contrast, accessibility, and responsive design.
- Ability to analyze user needs and convert them into simple interface flows.
- Basic design system awareness: components, variants, states, and handoff.
- Communication skills for explaining design choices.

Responsibilities:
- Create wireframes, UI screens, and prototypes from product requirements.
- Improve forms, dashboards, landing pages, and user journeys.
- Prepare assets and notes for developer handoff.
- Gather feedback and iterate on designs.
- Maintain consistency across components and screens.

Good resume signals:
- Figma portfolio, case studies, redesigns, app screens, or usability notes.
- Before/after improvements with reasoning.
- Evidence of responsive design, component systems, and product thinking.`,
  },
  {
    name: "Custom",
    level: "Custom",
    summary: "Paste or write a role manually when the listed templates do not fit.",
    skills: ["Manual input"],
    text: "",
  },
];

const JOB_OPTIONS = Object.fromEntries(ROLE_TEMPLATES.map((template) => [template.name, template.text]));

function loadStoredAnalysis() {
  try {
    const stored = window.localStorage.getItem("resume-ai-latest-analysis");
    return stored ? JSON.parse(stored) : null;
  } catch {
    return null;
  }
}

function getRoleTemplate(roleName) {
  return ROLE_TEMPLATES.find((template) => template.name === roleName) || ROLE_TEMPLATES[0];
}

function statusClass(status) {
  if (status === "Strong match") return "status-strong";
  if (status === "Moderate match") return "status-moderate";
  return "status-weak";
}

function SignalList({ signals }) {
  const uniqueSignals = useMemo(
    () => [...new Set(signals || [])].sort((a, b) => String(a).localeCompare(String(b))),
    [signals],
  );

  if (!uniqueSignals.length) {
    return <p className="empty-copy">No depth signals detected.</p>;
  }

  return (
    <div className="signal-list">
      {uniqueSignals.map((signal) => (
        <span className="signal-pill" key={signal}>
          {signal}
        </span>
      ))}
    </div>
  );
}

function FeedbackBlock({ feedback }) {
  if (!feedback) return null;
  const isError = feedback.startsWith("Error:");
  return <div className={isError ? "feedback-box error" : "feedback-box"}>{feedback}</div>;
}

function cleanReportText(text) {
  return String(text || "")
    .replace(/\*\*/g, "")
    .replace(/`/g, "")
    .replace(/^#{1,6}\s*/gm, "")
    .trim();
}

function buildReportSections(feedback) {
  const cleaned = cleanReportText(feedback);
  if (!cleaned) return [];

  const sections = [];
  let current = { title: "API feedback", lines: [] };

  cleaned.split("\n").forEach((rawLine) => {
    const line = rawLine.trim();
    if (!line || line === "---") return;

    const numberedHeading = line.match(/^(\d+)\.\s+(.+)/);
    const colonHeading = line.length < 76 && /^[A-Z][A-Za-z\s/+-]+:$/.test(line);
    const quickHeading = /^(Quick Wins|Bottom line|Resume vs\. Job|Why the|Practice Plan|Missing Skills)/i.test(line);

    if ((numberedHeading || colonHeading || quickHeading) && current.lines.length) {
      sections.push(current);
      current = { title: numberedHeading ? numberedHeading[2] : line.replace(/:$/, ""), lines: [] };
    } else if ((numberedHeading || colonHeading || quickHeading) && !current.lines.length) {
      current.title = numberedHeading ? numberedHeading[2] : line.replace(/:$/, "");
    } else {
      current.lines.push(line);
    }
  });

  if (current.lines.length || current.title !== "API feedback") {
    sections.push(current);
  }

  return sections.slice(0, 8);
}

function StructuredFeedback({ feedback }) {
  if (!feedback) return null;

  if (feedback.startsWith("Error:")) {
    return <div className="dashboard-report-error">{feedback}</div>;
  }

  const sections = buildReportSections(feedback);

  return (
    <div className="report-section-list">
      {sections.map((section, index) => (
        <article className="report-section" key={`${section.title}-${index}`}>
          <h3>{section.title}</h3>
          <div className="report-lines">
            {section.lines.map((line, lineIndex) => {
              const isBullet = /^[-•]\s+/.test(line);
              const isTable = line.includes("|");
              return (
                <p
                  className={`${isBullet ? "report-bullet" : ""} ${isTable ? "report-table-line" : ""}`}
                  key={`${line}-${lineIndex}`}
                >
                  {line.replace(/^[-•]\s+/, "")}
                </p>
              );
            })}
          </div>
        </article>
      ))}
    </div>
  );
}

function RoleDropdown({ selectedRole, onSelect }) {
  const [isOpen, setIsOpen] = useState(false);
  const selectedTemplate = getRoleTemplate(selectedRole);

  function chooseTemplate(templateName) {
    onSelect(templateName);
    setIsOpen(false);
  }

  return (
    <div className={`role-dropdown ${isOpen ? "open" : ""}`}>
      <button
        type="button"
        id="role-template"
        className="role-dropdown-trigger"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        onClick={() => setIsOpen((current) => !current)}
      >
        <span>
          <strong>{selectedTemplate.name}</strong>
          <small>{selectedTemplate.summary}</small>
        </span>
        <ChevronDown size={20} strokeWidth={2.6} />
      </button>

      {isOpen ? (
        <div className="role-dropdown-menu" role="listbox" aria-label="Role templates">
          {ROLE_TEMPLATES.map((template) => (
            <button
              type="button"
              className={`role-option ${template.name === selectedRole ? "selected" : ""}`}
              key={template.name}
              role="option"
              aria-selected={template.name === selectedRole}
              onClick={() => chooseTemplate(template.name)}
            >
              <span className="role-option-copy">
                <strong>{template.name}</strong>
                <small>{template.summary}</small>
              </span>
              <span className="thinking-dots" aria-hidden="true">
                <i />
                <i />
                <i />
              </span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

function HeroArt() {
  return (
    <svg className="hero-art" viewBox="0 0 560 430" role="img" aria-label="Resume analysis illustration">
      <defs>
        <linearGradient id="portal" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0" stopColor="#ffffff" stopOpacity="0.9" />
          <stop offset="1" stopColor="#9b2cff" stopOpacity="0.18" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="8" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <path
        className="hero-ribbon"
        d="M70 342 C142 280 199 312 264 348 C344 391 427 378 520 314"
        fill="none"
        stroke="#9b2cff"
        strokeWidth="24"
        strokeLinecap="round"
        opacity="0.5"
        filter="url(#glow)"
      />
      <g className="hero-orbit hero-resume">
        <rect x="92" y="88" width="160" height="210" rx="34" fill="rgba(255,255,255,0.09)" stroke="rgba(255,255,255,0.25)" />
        <rect x="126" y="124" width="92" height="128" rx="18" fill="url(#portal)" opacity="0.9" />
      </g>
      <g className="hero-orbit hero-check">
        <rect x="160" y="270" width="76" height="74" rx="12" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.34)" />
        <path d="M181 306 L196 321 L222 290" fill="none" stroke="#e8b6ff" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" />
      </g>
      <g className="hero-orbit hero-person hero-person-a">
        <circle cx="338" cy="184" r="35" fill="rgba(255,255,255,0.72)" />
        <path d="M302 270 C307 230 368 230 374 270 C360 286 319 286 302 270 Z" fill="rgba(255,255,255,0.62)" />
      </g>
      <g className="hero-orbit hero-person hero-person-b">
        <circle cx="458" cy="152" r="32" fill="rgba(255,255,255,0.55)" />
        <path d="M424 236 C430 199 486 199 492 236 C478 251 440 251 424 236 Z" fill="rgba(255,255,255,0.42)" />
      </g>
    </svg>
  );
}

function ResourcesPage() {
  const resources = [
    {
      icon: <FileSearch size={28} />,
      title: "Resume checklist",
      text: "Keep role keywords close to the work evidence: project scope, tools used, metrics, and business outcome.",
    },
    {
      icon: <Network size={28} />,
      title: "Skill gap map",
      text: "Group missing requirements into frontend, backend, data, cloud, and communication so practice stays organized.",
    },
    {
      icon: <ClipboardCheck size={28} />,
      title: "Project prompts",
      text: "Turn weak skills into proof by building one small project per gap and writing the result as a resume bullet.",
    },
    {
      icon: <GraduationCap size={28} />,
      title: "Interview prep",
      text: "Convert the match report into talking points: strongest overlap, missing areas, and what you are doing next.",
    },
  ];

  return (
    <main className="resource-page">
      <nav className="site-nav resource-nav" aria-label="Resource navigation">
        <a className="brand" href="#intro">
          <span className="brand-mark">V</span>
          <span>Resume AI</span>
        </a>
        <div className="nav-links">
          <a href="#matcher">Analyzer</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </div>
        <div className="nav-actions">
          <a className="nav-button light" href="#matcher">
            Back <span className="arrow-dot"><ArrowRight size={22} strokeWidth={3} /></span>
          </a>
        </div>
      </nav>

      <section className="resource-shell">
        <div className="resource-hero">
          <div>
            <div className="section-kicker">Get more resource</div>
            <h1>Resources for a stronger match.</h1>
            <p>
              Use these quick references after running the analyzer to improve the resume, close gaps,
              and prepare cleaner interview answers.
            </p>
          </div>
          <BookOpen size={86} strokeWidth={1.5} />
        </div>

        <div className="resource-grid">
          {resources.map((resource) => (
            <article className="resource-card" key={resource.title}>
              <div className="resource-icon">{resource.icon}</div>
              <h2>{resource.title}</h2>
              <p>{resource.text}</p>
            </article>
          ))}
        </div>

        <section className="resource-notes">
          <h2>Quick improvement path</h2>
          <ol>
            <li>Run the analyzer with the exact job description.</li>
            <li>Pick the lowest-signal skill area from the feedback.</li>
            <li>Build or rewrite one project bullet that proves that skill.</li>
            <li>Run the resume again and compare the score movement.</li>
          </ol>
        </section>
      </section>
    </main>
  );
}

function DashboardPage({ analysis, selectedRole, selectedTemplate, resumeFile }) {
  if (!analysis) {
    return (
      <main className="dashboard-empty-page">
        <nav className="site-nav dashboard-nav" aria-label="Dashboard navigation">
          <a className="brand" href="#intro">
            <span className="brand-mark">V</span>
            <span>Resume AI</span>
          </a>
          <div className="nav-links">
            <a href="#matcher">Analyzer</a>
            <a href="#resources">Resources</a>
          </div>
          <div className="nav-actions">
            <a className="nav-button light" href="#matcher">
              Run analysis <span className="arrow-dot"><ArrowRight size={22} strokeWidth={3} /></span>
            </a>
          </div>
        </nav>
        <section className="dashboard-empty">
          <h1>No analysis yet.</h1>
          <p>Upload a resume and run the analyzer to generate a live dashboard.</p>
          <a className="hero-cta" href="#matcher">
            Open analyzer <span className="arrow-dot"><ArrowRight size={22} strokeWidth={3} /></span>
          </a>
        </section>
      </main>
    );
  }

  const score = Number(analysis.score || 0);
  const similarityPercent = Math.round(Number(analysis.similarity || 0) * 100);
  const depthGap = Number(analysis.depth_gap || 0);
  const resumeSignalCount = new Set(analysis.resume_signals || []).size;
  const jdSignalCount = new Set(analysis.jd_signals || []).size;
  const resumeWords = (analysis.resume_preview || "").trim().split(/\s+/).filter(Boolean).length;
  const depthHealth = Math.max(0, Math.round(100 - depthGap * 25));
  const signalCoverage = Math.min(100, Math.round(((resumeSignalCount + jdSignalCount) / 8) * 100));
  const readiness = Math.round((score * 0.56) + (similarityPercent * 0.26) + (depthHealth * 0.12) + (signalCoverage * 0.06));
  const chartRows = [
    ["Match score", score],
    ["Semantic fit", similarityPercent],
    ["Depth health", depthHealth],
    ["Signal coverage", signalCoverage],
    ["Resume volume", Math.min(100, Math.round(resumeWords / 12))],
    ["Readiness", readiness],
  ];
  const kpis = [
    {
      icon: <Gauge size={22} />,
      label: "Overall Match",
      value: `${score.toFixed(2)}%`,
      detail: analysis.status,
      tone: score >= 70 ? "up" : "down",
      description: "The final computed match score combining semantic similarity and depth health."
    },
    {
      icon: <Eye size={22} />,
      label: "Semantic Similarity",
      value: Number(analysis.similarity || 0).toFixed(2),
      detail: "TF-IDF cosine similarity",
      tone: similarityPercent >= 50 ? "up" : "down",
      description: "How well the resume's language matches the job description based on text overlap."
    },
    {
      icon: <Layers size={22} />,
      label: "Depth Gap",
      value: depthGap,
      detail: "Skill-depth mismatch",
      tone: depthGap <= 1 ? "up" : "down",
      description: "The penalty applied based on missing crucial skills and lack of depth."
    },
    {
      icon: <Target size={22} />,
      label: "Signal Coverage",
      value: `${signalCoverage}%`,
      detail: `${resumeSignalCount + jdSignalCount} detected signals`,
      tone: signalCoverage >= 45 ? "up" : "down",
      description: "Percentage of key signals from the role template detected in your resume."
    },
    {
      icon: <FileText size={22} />,
      label: "Resume Words",
      value: resumeWords,
      detail: analysis.resume_file_name || resumeFile?.name || "Extracted preview",
      tone: resumeWords >= 120 ? "up" : "down",
      description: "The total number of words successfully extracted from your uploaded resume."
    },
  ];

  return (
    <main className="dashboard-page">
      <aside className="dashboard-sidebar" aria-label="Dashboard sections">
        <a className="dash-mark" href="#intro">V</a>
        <a className="dash-side-link active" href="#dashboard"><BarChart3 size={20} />Dashboard</a>
        <a className="dash-side-link" href="#matcher"><FileSearch size={20} />Analyzer</a>
        <a className="dash-side-link" href="#resources"><BookOpen size={20} />Resources</a>
        <a className="dash-side-link" href="#dashboard-report"><Brain size={20} />Report</a>
      </aside>

      <section className="dashboard-main">
        <header className="dashboard-topbar">
          <div>
            <h1>Analysis dashboard</h1>
            <p>{selectedRole} match report generated from the latest resume upload.</p>
          </div>
          <div className="dashboard-actions">
            <a className="nav-button" href="#matcher">Run another</a>
          </div>
        </header>

        <div className="dashboard-filterbar">
          <div>
            <span>Role template</span>
            <strong>{analysis.role_template || selectedTemplate.name}</strong>
          </div>
          <div>
            <span>Experience level</span>
            <strong>{selectedTemplate.level}</strong>
          </div>
          <div>
            <span>Resume file</span>
            <strong>{analysis.resume_file_name || resumeFile?.name || "Uploaded resume"}</strong>
          </div>
          <div>
            <span>Match status</span>
            <div style={{ display: 'flex', alignItems: 'center', height: '100%', marginTop: '2px' }}>
              <span className={`status-box ${statusClass(analysis.status)}`} style={{ display: 'inline-flex' }}>{analysis.status}</span>
            </div>
          </div>
        </div>

        <div className="dashboard-kpis">
          {kpis.map((kpi) => (
            <article className="dash-kpi-card" key={kpi.label} data-tooltip={kpi.description}>
              <div className="dash-kpi-head">
                <span>{kpi.icon}</span>
                {kpi.tone === "up" ? <TrendingUp size={18} /> : <TrendingDown size={18} />}
              </div>
              <p>{kpi.label}</p>
              <strong>{kpi.value}</strong>
              <small>{kpi.detail}</small>
            </article>
          ))}
        </div>

        <section className="dashboard-panel performance-panel">
          <div className="dashboard-panel-head">
            <div>
              <h2>Live performance</h2>
              <p>Derived from the latest scorer response. Values update each time a new resume is analyzed.</p>
            </div>
            <div className="chart-legend">
              <span><i /> Current resume</span>
              <span><i /> Target threshold</span>
            </div>
          </div>
          <div className="dashboard-chart">
            {chartRows.map(([label, value]) => (
              <div className="chart-row" key={label}>
                <span>{label}</span>
                <div className="chart-track">
                  <i style={{ width: `${Math.max(3, Math.min(100, value))}%` }} />
                  <b />
                </div>
                <strong>{Math.round(value)}%</strong>
              </div>
            ))}
          </div>
        </section>

        <section className="dashboard-grid-two">
          <article className="dashboard-panel" id="dashboard-report">
            <div className="dashboard-panel-head">
              <div>
                <h2>API feedback report</h2>
                <p>Structured from the feedback response so the recommendation is easier to read.</p>
              </div>
            </div>
            <StructuredFeedback feedback={analysis.feedback} />
          </article>

          <aside className="dashboard-panel signal-dashboard-card">
            <h2>Signal review</h2>
            <div className="signal-block">
              <h3>Resume signals</h3>
              <SignalList signals={analysis.resume_signals} />
            </div>
            <div className="signal-block">
              <h3>Job description signals</h3>
              <SignalList signals={analysis.jd_signals} />
            </div>
            <details className="dashboard-preview">
              <summary>Preview extracted resume text</summary>
              <pre>{analysis.resume_preview?.trim() || "No text extracted from the uploaded file."}</pre>
            </details>
          </aside>
        </section>
      </section>
    </main>
  );
}

function AnalyzerPage({
  selectedRole,
  selectedTemplate,
  jobDescription,
  resumeFile,
  loading,
  message,
  onRoleChange,
  onJobDescriptionChange,
  onResumeFileChange,
  onRunAnalysis,
}) {
  return (
    <main className="analyzer-page">
      <nav className="site-nav analyzer-nav" aria-label="Analyzer navigation">
        <a className="brand" href="#intro">
          <span className="brand-mark">V</span>
          <span>Resume AI</span>
        </a>
        <div className="nav-links">
          <a href="#intro">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
        </div>
        <div className="nav-actions">
          <a className="nav-button" href="#resources">
            Get more resource
          </a>
          <a className="nav-button light" href="#intro">
            Back <span className="arrow-dot"><ArrowRight size={22} strokeWidth={3} /></span>
          </a>
        </div>
      </nav>

      <section className="matcher-shell" id="matcher">
        <div className="matcher-header">
          <div className="section-kicker">Resume analyzer</div>
          <h2 className="section-heading">Run the actual match here.</h2>
          <p className="section-copy">
            This is the main workflow: upload the resume, choose or paste the role, and run the local ML scorer.
          </p>
        </div>

        <form className="analyzer-grid" onSubmit={onRunAnalysis}>
          <section className="form-panel">
            <h3 className="panel-heading">Target role</h3>
            <p className="panel-note">Choose a starter role or paste the exact job description you want to compare against.</p>
            <label htmlFor="role-template">Role template</label>
            <RoleDropdown selectedRole={selectedRole} onSelect={onRoleChange} />
            {selectedTemplate.name !== "Custom" ? (
              <div className="template-helper" aria-label="Selected template details">
                <div>
                  <strong>{selectedTemplate.level} template</strong>
                  <p>{selectedTemplate.summary}</p>
                </div>
                <div className="template-skill-list">
                  {selectedTemplate.skills.map((skill) => (
                    <span key={skill}>{skill}</span>
                  ))}
                </div>
              </div>
            ) : (
              <div className="template-helper">
                <strong>Custom template</strong>
                <p>Write or paste the exact role. The analyzer will still score the resume against whatever you enter.</p>
              </div>
            )}
            <label htmlFor="job-description">Job description</label>
            <textarea
              id="job-description"
              value={jobDescription}
              onChange={onJobDescriptionChange}
              placeholder="Paste the target job description here."
              rows={10}
            />
          </section>

          <section className="form-panel">
            <h3 className="panel-heading">Candidate resume</h3>
            <p className="panel-note">Upload a PDF or image resume. The app extracts text locally before scoring.</p>
            <label htmlFor="resume-file">Resume file</label>
            <div className="upload-box">
              <input
                id="resume-file"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={(event) => onResumeFileChange(event.target.files?.[0] || null)}
              />
              <Upload size={28} />
              <span>{resumeFile ? resumeFile.name : "Choose PDF, PNG, JPG, or JPEG"}</span>
            </div>
            <button className="run-button" disabled={loading} type="submit">
              {loading ? "Analyzing resume..." : "Run analysis"}
            </button>
            <a className="resource-tab" href="#resources">
              Get more resource <ArrowRight size={18} strokeWidth={3} />
            </a>
            {message ? <div className="notice">{message}</div> : null}
          </section>
        </form>

      </section>
    </main>
  );
}

function App() {
  const [selectedRole, setSelectedRole] = useState("Frontend Developer");
  const [jobDescription, setJobDescription] = useState(JOB_OPTIONS["Frontend Developer"]);
  const [resumeFile, setResumeFile] = useState(null);
  const [analysis, setAnalysis] = useState(() => loadStoredAnalysis());
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [route, setRoute] = useState(window.location.hash || "#intro");

  useEffect(() => {
    function syncRoute() {
      setRoute(window.location.hash || "#intro");
    }

    window.addEventListener("hashchange", syncRoute);
    return () => window.removeEventListener("hashchange", syncRoute);
  }, []);

  function handleRoleChange(role) {
    setSelectedRole(role);
    if (role !== "Custom") {
      setJobDescription(JOB_OPTIONS[role]);
    }
  }

  async function runAnalysis(event) {
    event.preventDefault();
    setMessage("");

    if (!resumeFile || !jobDescription.trim()) {
      setMessage("Please upload a resume and add a job description before running analysis.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job_description", jobDescription);

    setLoading(true);
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Analysis failed.");
      }
      const nextAnalysis = {
        ...data,
        resume_file_name: resumeFile?.name || "Uploaded resume",
        role_template: selectedRole,
      };
      setAnalysis(nextAnalysis);
      window.localStorage.setItem("resume-ai-latest-analysis", JSON.stringify(nextAnalysis));
      window.location.hash = "#dashboard";
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  if (route === "#resources") {
    return <ResourcesPage />;
  }

  if (route === "#dashboard") {
    return (
      <DashboardPage
        analysis={analysis}
        selectedRole={selectedRole}
        selectedTemplate={getRoleTemplate(selectedRole)}
        resumeFile={resumeFile}
      />
    );
  }

  if (route === "#matcher") {
    return (
      <AnalyzerPage
        selectedRole={selectedRole}
        selectedTemplate={getRoleTemplate(selectedRole)}
        jobDescription={jobDescription}
        resumeFile={resumeFile}
        loading={loading}
        message={message}
        onRoleChange={handleRoleChange}
        onJobDescriptionChange={(event) => {
          setJobDescription(event.target.value);
          if (selectedRole !== "Custom") setSelectedRole("Custom");
        }}
        onResumeFileChange={setResumeFile}
        onRunAnalysis={runAnalysis}
      />
    );
  }

  return (
    <main className="intro-page">
      <section className="hero" id="intro">
        <nav className="site-nav" aria-label="Main navigation">
          <a className="brand" href="#intro">
            <span className="brand-mark">V</span>
            <span>Resume AI</span>
          </a>
          <div className="nav-links">
            <a href="#matcher">Analyzer</a>
            <a href="#features">Features</a>
            <a href="#how-it-works">How it works</a>
          </div>
          <div className="nav-actions">
            <a className="nav-button" href="#workflow">
              Workflow
            </a>
            <a className="nav-button light" href="#matcher">
              Start <span className="arrow-dot"><ArrowRight size={22} strokeWidth={3} /></span>
            </a>
          </div>
        </nav>

        <div className="hero-grid">
          <div>
            <h1 className="hero-title">
              Stop guessing. Start matching <span>resumes.</span>
            </h1>
            <p className="hero-copy">
              Compare a candidate resume with a target job description using local ML scoring,
              then review concise AI feedback for gaps, signals, and next steps.
            </p>
            <a className="hero-cta" href="#matcher">
              Try it now <span className="arrow-dot"><ArrowRight size={23} strokeWidth={3} /></span>
            </a>
          </div>
          <div className="floating-chips">
            <a className="chip-link chip-1" href="#features">
              <Sparkles size={18} /> Local score, API feedback
            </a>
            <a className="chip-link chip-2" href="#matcher">
              <Upload size={18} /> PDF and image resume upload
            </a>
            <a className="chip-link chip-3" href="#how-it-works">
              <Check size={18} /> Skill-depth signal review
            </a>
            <HeroArt />
          </div>
        </div>
      </section>

      <section className="feature-band" id="features">
        <div className="feature-head">
          <div className="section-kicker">Main features</div>
          <h2 className="section-heading">Power up your <span>resume review</span></h2>
          <p className="section-copy">
            The extra sections below explain what the app does without pushing the real analyzer out of the way.
          </p>
        </div>
        <div className="feature-grid">
          <a className="feature-link" href="#matcher">
            <article className="feature-card">
              <div className="feature-art"><Network size={64} /></div>
              <h3>Smart matching</h3>
              <p>TF-IDF similarity compares the cleaned resume and role text locally before feedback is requested.</p>
            </article>
          </a>
          <a className="feature-link" href="#matcher">
            <article className="feature-card">
              <div className="feature-art"><BarChart3 size={64} /></div>
              <h3>Score dashboard</h3>
              <p>Overall match, semantic similarity, and skill depth gap stay visible after each analysis run.</p>
            </article>
          </a>
          <a className="feature-link" href="#how-it-works">
            <article className="feature-card">
              <div className="feature-art"><FileSearch size={64} /></div>
              <h3>Signal review</h3>
              <p>Depth cues such as basic, learning, advanced, and expert are surfaced for easier interpretation.</p>
            </article>
          </a>
        </div>
        <div className="contact-card" id="contact">
          <strong>Need to tune the analysis?</strong>
          <p className="empty-copy">Use the role template and job description above to make the score more specific to the position.</p>
        </div>
      </section>

      <section className="how-band" id="how-it-works">
        <div className="how-grid">
          <div>
            <div className="section-kicker dark">How it works</div>
            <h2 className="how-title">From upload to <span>matched signal.</span></h2>
            <p className="how-copy">
              The app keeps the important workflow local first, then uses an LLM only to explain the result in plain language.
            </p>
          </div>
          <div>
            <div className="step-card"><strong>01. Extract text</strong><span>PDF and image resumes are converted into text for analysis.</span></div>
            <div className="step-card"><strong>02. Clean and normalize</strong><span>Resume and job-description text are preprocessed into comparable feature text.</span></div>
            <div className="step-card"><strong>03. Score and explain</strong><span>The local model computes the percentage match, then API feedback explains the gaps.</span></div>
          </div>
        </div>
      </section>

      <section className="workflow-band" id="workflow">
        <div className="workflow-wrap">
          <div className="workflow-head">
            <div>
              <div className="section-kicker">Workflow</div>
              <h2 className="section-heading">Animated working flow</h2>
            </div>
            <p className="section-copy">
              A quick view of how the page moves from user input to a scored resume match.
            </p>
          </div>
          <div className="workflow-chart" aria-label="Animated resume matcher workflow">
            <svg className="workflow-wave" viewBox="0 0 1000 160" aria-hidden="true" preserveAspectRatio="none">
              <path
                className="workflow-wave-path"
                d="M40 86 C130 18 210 18 300 86 S470 154 560 86 S730 18 820 86 S930 154 970 86"
              />
              <circle className="workflow-wave-ball" r="12">
                <animateMotion
                  dur="5.6s"
                  repeatCount="indefinite"
                  path="M40 86 C130 18 210 18 300 86 S470 154 560 86 S730 18 820 86 S930 154 970 86"
                />
              </circle>
            </svg>
            <div className="workflow-flow">
              {[
                ["01", "Upload resume", "PDF or image file enters the analyzer."],
                ["02", "Extract text", "PyPDF2 or OCR reads the resume content."],
                ["03", "Preprocess", "Resume and role text are cleaned and normalized."],
                ["04", "Compare", "TF-IDF similarity checks resume against the job."],
                ["05", "Score match", "Similarity and depth gap become one match score."],
                ["06", "Show results", "Dashboard, signals, and AI feedback appear on page."],
              ].map(([number, label, detail]) => (
                <div className="workflow-step" key={number}>
                  <span className="workflow-dot">{number}</span>
                  <strong className="workflow-label">{label}</strong>
                  <p className="workflow-detail">{detail}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
