import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.scss'
})
export class ForgotPasswordComponent implements OnInit {
  forgotPasswordForm!: FormGroup;
  isLoading = false;
  errorMessage = '';
  successMessage = '';
  emailSent = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
  }

  private initForm(): void {
    this.forgotPasswordForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
  }

  onSubmit(): void {
    if (this.forgotPasswordForm.valid) {
      this.isLoading = true;
      this.errorMessage = '';
      this.successMessage = '';

      const { email } = this.forgotPasswordForm.value;

      this.authService.forgotPassword(email).subscribe({
        next: (response) => {
          this.isLoading = false;
          this.emailSent = true;
          this.successMessage = 'Email enviado com sucesso! Verifique sua caixa de entrada.';
        },
        error: (error) => {
          this.isLoading = false;
          this.errorMessage = error.error?.detail || error.error?.message || 'Erro ao enviar email. Tente novamente.';
        }
      });
    } else {
      this.forgotPasswordForm.get('email')?.markAsTouched();
    }
  }

  get email() {
    return this.forgotPasswordForm.get('email');
  }

  goToLogin(): void {
    this.router.navigate(['/auth/login']);
  }
}
