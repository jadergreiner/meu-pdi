import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface User {
  id: string;
  nome_completo: string;
  email: string;
  email_validado: boolean;
  data_cadastro: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<User | null>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Load user from localStorage on service initialization (only in browser)
    if (isPlatformBrowser(this.platformId)) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        // TODO: Validate token and load user data
      }
    }
  }

  get currentUser(): User | null {
    return this.currentUserSubject.value;
  }

  isAuthenticated(): boolean {
    if (isPlatformBrowser(this.platformId)) {
      return !!localStorage.getItem('auth_token');
    }
    return false;
  }

  login(credentials: { email: string; senha: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>('/api/auth/login', credentials).pipe(
      tap(response => {
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('auth_token', response.access_token);
          localStorage.setItem('refresh_token', response.refresh_token);
        }
        this.currentUserSubject.next(response.user);
      })
    );
  }

  register(userData: { nome_completo: string; email: string; senha: string; confirmar_senha: string; aceitar_termos: boolean }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>('/api/auth/register', userData).pipe(
      tap(response => {
        if (isPlatformBrowser(this.platformId)) {
          localStorage.setItem('auth_token', response.access_token);
          localStorage.setItem('refresh_token', response.refresh_token);
        }
        this.currentUserSubject.next(response.user);
      })
    );
  }

  logout(): void {
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('refresh_token');
    }
    this.currentUserSubject.next(null);
  }

  refreshToken(): Observable<{ access_token: string; token_type: string }> {
    if (!isPlatformBrowser(this.platformId)) {
      throw new Error('Cannot refresh token on server side');
    }

    const refreshToken = localStorage.getItem('refresh_token');
    return this.http.post<{ access_token: string; token_type: string }>('/api/auth/refresh', { refresh_token: refreshToken }).pipe(
      tap(response => {
        localStorage.setItem('auth_token', response.access_token);
      })
    );
  }

  forgotPassword(email: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>('/api/auth/reset-password', { email });
  }

  resetPassword(token: string, newPassword: string): Observable<{ message: string }> {
    return this.http.post<{ message: string }>('/api/auth/confirm-reset-password', {
      token,
      nova_senha: newPassword,
      confirmar_senha: newPassword
    });
  }
}
