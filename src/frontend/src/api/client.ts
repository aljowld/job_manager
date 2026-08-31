const DEFAULT_API_BASE_URL = 'http://localhost:8000/api/v1';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL).replace(
  /\/+$/,
  '',
);

type QueryParams = Record<string, string | number | boolean | undefined>;

/** Thrown for non-2xx responses (`status` is the HTTP code) and network failures (`status = 0`). */
export class ApiError extends Error {
  readonly status: number;
  readonly code?: string;

  constructor(message: string, status: number, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

function buildUrl(path: string, params?: QueryParams): string {
  const url = new URL(`${API_BASE_URL}${path}`);
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined) {
        url.searchParams.set(key, String(value));
      }
    }
  }
  return url.toString();
}

async function extractErrorDetails(response: Response): Promise<{ message: string; code?: string }> {
  try {
    const body = (await response.json()) as { error?: { message?: string; code?: string } };
    if (body.error?.message) {
      return { message: body.error.message, code: body.error.code };
    }
  } catch {
    // response body was not JSON, or did not match the project's error shape
  }
  return { message: response.statusText || `Request failed with status ${response.status}` };
}

/** Minimal fetch wrapper: builds the URL, surfaces non-2xx/network failures as `ApiError`. */
export async function request<T>(
  path: string,
  params?: QueryParams,
  options?: RequestInit,
): Promise<T> {
  const url = buildUrl(path, params);
  let response: Response;
  try {
    response = await fetch(url, options);
  } catch {
    throw new ApiError('Network error: could not reach the API', 0);
  }

  if (!response.ok) {
    const { message, code } = await extractErrorDetails(response);
    throw new ApiError(message, response.status, code);
  }

  return (await response.json()) as T;
}
