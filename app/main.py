from contextlib import asynccontextmanager
import logging

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)

from fastapi.exceptions import RequestValidationError

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.core.config import settings
from app.db.session import init_db, AsyncSessionLocal
from app.models.permission import Permission

from app.routes import (
    user,auth,role,department,permission
)

# from app.middleware.auth_middleware import (   
#     RequestLoggingMiddleware,
#     SecurityHeadersMiddleware,
# )

from app.models.role import Role
from app.models.departments import Department


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


# =========================================================
# DEFAULT ROLES
# =========================================================

DEFAULT_ROLES = [
    {
        "role_name": "Admin",
        "description": "System administrator",
    },
    {
        "role_name": "Manager",
        "description": "Project manager",
    },
    {
        "role_name": "Staff",
        "description": "Normal staff user",
    },
]


# =========================================================
# DEFAULT DEPARTMENTS
# =========================================================

DEFAULT_DEPARTMENTS = [
    {
        "name": "Administration",
        "description": "Administration department",
    },
    {
        "name": "Marketing",
        "description": "Marketing department",
    },
    {
        "name": "Development",
        "description": "Software development department",
    },
    {
        "name": "Design",
        "description": "UI UX design department",
    },
]


#default permissions


DEFAULT_PERMISSIONS = [

    # USERS
    ("user", "create", "Create users"),
    ("user", "view", "View users"),
    ("user", "edit", "Edit users"),
    ("user", "delete", "Delete users"),

    # ROLES
    ("roles", "create", "Create roles"),
    ("roles", "view", "View roles"),
    ("roles", "edit", "Edit roles"),
    ("roles", "delete", "Delete roles"),

    # DEPARTMENTS
    ("departments", "create", "Create departments"),
    ("departments", "view", "View departments"),
    ("departments", "edit", "Edit departments"),
    ("departments", "delete", "Delete departments"),

    # CUSTOMERS
    ("customers", "create", "Create customers"),
    ("customers", "view", "View customers"),
    ("customers", "edit", "Edit customers"),
    ("customers", "delete", "Delete customers"),

    # ENQUIRIES
    ("enquiries", "create", "Create enquiries"),
    ("enquiries", "view", "View enquiries"),
    ("enquiries", "edit", "Edit enquiries"),
    ("enquiries", "delete", "Delete enquiries"),

    # QUOTATIONS
    ("quotations", "create", "Create quotations"),
    ("quotations", "view", "View quotations"),
    ("quotations", "approve", "Approve quotations"),
    ("quotations", "reject", "Reject quotations"),

    # PROJECTS
    ("projects", "create", "Create projects"),
    ("projects", "view", "View projects"),
    ("projects", "edit", "Edit projects"),
    ("projects", "delete", "Delete projects"),

    # TASKS
    ("tasks", "create", "Create tasks"),
    ("tasks", "assign", "Assign tasks"),
    ("tasks", "view", "View tasks"),
    ("tasks", "edit", "Edit tasks"),
    ("tasks", "delete", "Delete tasks"),

    # REPORTS
    ("reports", "create", "Create reports"),
    ("reports", "view", "View reports"),

    # FEEDBACK
    ("feedback", "create", "Create feedback"),
    ("feedback", "view", "View feedback"),

    # NOTIFICATIONS
    ("notifications", "view", "View notifications"),
]


#seed permissions

async def seed_permissions():

    async with AsyncSessionLocal() as db:

        for module, action, description in DEFAULT_PERMISSIONS:

            permission_code = f"{module}:{action}"

            result = await db.execute(
                select(Permission).where(
                    Permission.code == permission_code
                )
            )

            existing_permission = result.scalar_one_or_none()

            if not existing_permission:

                permission = Permission(

                    module=module,

                    action=action,

                    code=permission_code,

                    description=description,
                )

                db.add(permission)

        await db.commit()

        logger.info("Default permissions seeded")

# seed roles


async def seed_roles():

    async with AsyncSessionLocal() as db:

        for role_data in DEFAULT_ROLES:

            result = await db.execute(
                select(Role).where(
                    Role.role_name == role_data["role_name"]
                )
            )

            existing_role = result.scalar_one_or_none()

            if not existing_role:

                role = Role(
                    role_name=role_data["role_name"],
                    description=role_data["description"],
                )

                db.add(role)

        await db.commit()

        logger.info("Default roles seeded")



#seed departments

async def seed_departments():

    async with AsyncSessionLocal() as db:

        for department_data in DEFAULT_DEPARTMENTS:

            result = await db.execute(
                select(Department).where(
                    Department.name == department_data["name"]
                )
            )

            existing_department = result.scalar_one_or_none()

            if not existing_department:

                department = Department(
                    name=department_data["name"],
                    description=department_data["description"],
                )

                db.add(department)

        await db.commit()

        logger.info("Default departments seeded")


async def seed_admin_user():

    from sqlalchemy import select

    from app.models.user import User, UserStatus

    from app.core.security import get_password_hash

    async with AsyncSessionLocal() as db:

        # Check admin already exists
        result = await db.execute(
            select(User).where(
                User.email == "admin@gmail.com"
            )
        )

        existing_admin = result.scalar_one_or_none()

        if existing_admin:

            logger.info("Admin user already exists")

            return

        # Get Admin Role
        role_result = await db.execute(
            select(Role).where(
                Role.role_name == "Admin"
            )
        )

        admin_role = role_result.scalar_one_or_none()

        if not admin_role:

            logger.error("Admin role not found")

            return

        # Get Administration Department
        department_result = await db.execute(
            select(Department).where(
                Department.name == "Administration"
            )
        )

        admin_department = department_result.scalar_one_or_none()

        if not admin_department:

            logger.error("Administration department not found")

            return

        # Create Admin User
        admin_user = User(

            name="Super Admin",

            email="admin@gmail.com",

            phone="9999999999",

            password=get_password_hash(
                "Admin@123"
            ),

            role_id=admin_role.id,

            department_id=admin_department.id,

            status=UserStatus.ACTIVE,
        )

        db.add(admin_user)

        await db.commit()

        logger.info("Default admin user created")


#life span


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        f"Starting {settings.PROJECT_NAME}"
    )

    # Initialize Database
    await init_db()

    # Seed master data
    await seed_roles()
    await seed_departments()
    await seed_admin_user()
    await seed_permissions()

    yield

    logger.info("Application shutdown")

#app


app = FastAPI(

    title=settings.PROJECT_NAME,

    version="1.0.0",

    description="""
# CRM Workflow Management System API

The CRM system manages the complete workflow for digital marketing,
software development, and project management operations.

---

## Features

- Authentication & Authorization
- Role & Permission Management
- Department Management
- Customer Management
- Enquiry Workflow
- Quotation Approval System
- Project Management
- Task Allocation
- Daily Work Reports
- Feedback System
- Notifications

---

## Workflow

Customer
→ Enquiry
→ Quotation
→ Project
→ Tasks
→ Reports
→ Feedback
    """,

    docs_url="/api/v1/docs",

    redoc_url="/api/v1/redoc",

    openapi_url="/api/v1/openapi.json",

    lifespan=lifespan,
)


# exception handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(
    _: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors()
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(
    _: Request,
    exc: IntegrityError,
):

    logger.exception(
        "Integrity Error",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=409,
        content={
            "detail": "Database constraint violated"
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    _: Request,
    exc: Exception,
):

    logger.exception(
        "Unhandled Exception",
        exc_info=exc,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        },
    )




origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#routers

API_PREFIX = "/api/v1"


app.include_router(
    user.router,
    prefix=API_PREFIX,
)
app.include_router(
    auth.router,
    prefix=API_PREFIX,
)   
app.include_router(
    role.router,
    prefix=API_PREFIX,
)
app.include_router(
    department.router,
    prefix=API_PREFIX,
)
app.include_router(
    permission.router,
    prefix=API_PREFIX,
)



