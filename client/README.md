# AutoCare Frontend

Vanilla HTML, CSS, and JavaScript frontend for the existing Django REST API. No Node.js, React, or frontend framework is required.

## Run locally

1. Start the Django API from `server/` using the project's existing virtual environment and environment variables.
2. Open `client/index.html` through a static web server (for example, VS Code Live Server).
3. Set `API_BASE_URL` in `js/config.js` to the Django API origin. The default is `http://127.0.0.1:8000`.
4. If the frontend and API use different origins, configure CORS on Django for the frontend origin. For production, preferably serve the frontend and API behind one HTTPS origin or configure a strict CORS allow-list. Do not use wildcard origins with credentials.

## Existing API contract

All paths below are relative to the API base URL. Protected endpoints use `Authorization: Bearer <access>`. Login returns SimpleJWT's `access` and `refresh` tokens with custom `email` and `role` claims in the token.

| Feature | Method and path | Access / payload |
|---|---|---|
| Register customer | POST `/api/auth/register/` | Public: `username,email,password,phone,name,address` |
| Login | POST `/api/auth/login/` | Public: `username,password`; returns access/refresh |
| Refresh | POST `/api/auth/token/refresh/` | Public: `refresh` |
| Current user | GET `/api/auth/me/` | Authenticated |
| Customer list/create | GET/POST `/customer/` | Admin; customer fields from CustomerSerializer |
| Customer detail | GET/PUT/PATCH/DELETE `/customer/{id}/` | Admin |
| Own customer profile | GET/PUT/PATCH `/customer/me/` | Customer; fields `name,phone,address` |
| Vehicles | GET/POST `/vehicle/` | Admin/customer; customer sees own vehicles |
| Vehicle detail | GET/PUT/PATCH/DELETE `/vehicle/{id}/` | Admin; customer own vehicle except delete |
| Jobs | GET/POST `/jobs/` | Admin creates; customers see own; mechanics see assigned |
| Job detail | GET/PUT/PATCH/DELETE `/jobs/{id}/` | Admin edits/deletes; customer/mechanic read scoped jobs |
| Job transition | POST `/jobs/{id}/transition/` | Admin or assigned mechanic; `{ "status": "in_progress" }` etc. |
| Send estimate | POST `/jobs/{id}/estimate/send/` | Admin; optional `{ "notes": "" }` |
| Estimate detail | GET `/jobs/{id}/estimate/` | Admin/customer/mechanic with job access |
| Estimate response | POST `/jobs/{id}/estimate/respond/` | Customer owner; `{ "approve": true }` or false |
| Mechanic assignments | GET/POST `/jobs/assign-mechanic/`; detail `/jobs/assign-mechanic/{id}/` | Admin; fields `job,mechanic,working_hours` |
| Job parts | GET/POST `/jobs/job-parts/`; detail `/jobs/job-parts/{id}/` | Admin or assigned mechanic; create uses `job,part,quantity` |
| Mechanics | GET/POST `/mechanics/`; detail `/mechanics/{id}/` | Admin manages; mechanic reads own profile |
| Specializations | GET/POST `/mechanics/specializations/`; detail `/mechanics/specializations/{id}/` | Admin |
| Parts inventory | GET/POST `/parts/`; detail `/parts/{id}/` | Admin |
| Repair photos | GET/POST `/photos/`; detail `/photos/{id}/` | Admin/customer/mechanic scoped; POST multipart `job,image,caption` |
| Invoices | GET `/payments/invoices/`; detail `/payments/invoices/{id}/` | Admin/customer owner |
| Generate invoice | POST `/payments/jobs/{job_id}/generate-invoice/` | Admin; `discount,tax_percent` |
| Payments for invoice | GET/POST `/payments/invoices/{id}/payments/` | Admin records `amount,method,reference`; customer can read |
| Receipts | GET `/payments/receipts/`; detail `/payments/receipts/{id}/` | Admin/customer owner |

## Important workflow rules

- Registration always creates a customer. Admin creates mechanic accounts; role selection is not public.
- Job status changes must use the transition endpoint, not edit the job directly.
- Estimate inventory deduction occurs in the backend only after customer approval.
- Invoices can be generated only for completed jobs with approved estimates.
- Payment recording is admin-only. There is no online payment gateway in this API.
- Repair photo upload must use `FormData`; do not manually set the multipart content type.
- Pagination is page-number based (`page`, optional `page_size`, maximum 100). API list responses may be paginated objects with `results` and `next/previous`.

## Known backend integration notes

- `DEBUG` in `server/config/settings.py` is currently read as a string. A string such as `"false"` is truthy in Python; cast it to Boolean before production use.
- Customer profile `patch = put` currently makes PATCH require a complete profile payload.
- Some views declare `search_fields` and/or `ordering_fields` without enabling DRF's SearchFilter/OrderingFilter. The frontend should not assume those query parameters work until the backend is corrected.
- The project settings do not currently configure CORS. A separate frontend origin needs a strict CORS configuration or same-origin reverse proxy.
- This frontend documents the checked-in API routes; run backend tests and browser integration tests in the deployment environment before production.

## Security

Tokens are held in session storage for the current browser tab and cleared on logout. Never put credentials, secret keys, or long-lived secrets in frontend source. The frontend hides controls by role for usability; Django permissions and scoped querysets remain the security boundary.
