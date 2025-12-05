import { Component, OnInit, OnDestroy, signal, computed } from '@angular/core';
import { Router } from '@angular/router';
import { Subject, takeUntil, forkJoin } from 'rxjs';
import { AuthService, User } from '../../core/services/auth.service';
import { HttpClient } from '@angular/common/http';

interface UserProfile {
  id: string;
  nome_completo: string;
  email: string;
  email_validado: boolean;
  data_cadastro: string;
}

interface PDIOverview {
  status_geral: string;
  objetivos_ativos: number;
  progresso_percentual: number;
  proximas_acoes: string[];
  ultima_atualizacao: string;
}

interface NextStep {
  titulo: string;
  descricao: string;
  prioridade: 'alta' | 'media' | 'baixa';
  url: string;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  // Signals para estado reativo
  isLoading = signal(true);
  error = signal<string | null>(null);
  profile = signal<UserProfile | null>(null);
  pdiOverview = signal<PDIOverview | null>(null);
  nextSteps = signal<NextStep[]>([]);

  // Computed signals
  userName = computed(() => {
    const profile = this.profile();
    return profile ? profile.nome_completo.split(' ')[0] : '';
  });

  fullUserName = computed(() => {
    const profile = this.profile();
    return profile ? profile.nome_completo : '';
  });

  constructor(
    private authService: AuthService,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadDashboardData(): void {
    this.isLoading.set(true);
    this.error.set(null);

    // TASK-014: Implementar Dashboard PDI Funcional - URLs corrigidas para endpoints reais
    forkJoin({
      profile: this.http.get<UserProfile>('/api/users/profile'),
      pdiOverview: this.http.get<PDIOverview>('/api/pdi/overview'),
      nextSteps: this.http.get<{ acoes_recomendadas: NextStep[] }>('/api/pdi/next-steps')
    }).pipe(
      takeUntil(this.destroy$)
    ).subscribe({
      next: (results) => {
        this.profile.set(results.profile);
        this.pdiOverview.set(results.pdiOverview);
        this.nextSteps.set(results.nextSteps.acoes_recomendadas || []);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Dashboard error:', err.error || err.message || err);
        this.error.set('Erro ao carregar dados do dashboard. Tente novamente.');
        this.isLoading.set(false);
      }
    });
  }

  onLogout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  onRetry(): void {
    this.loadDashboardData();
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'iniciando': return 'bg-blue-100 text-blue-800';
      case 'em_andamento': return 'bg-yellow-100 text-yellow-800';
      case 'concluido': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  getPriorityColor(prioridade: string): string {
    switch (prioridade) {
      case 'alta': return 'bg-red-100 text-red-800 border-red-200';
      case 'media': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'baixa': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  }

  getPriorityBadgeColor(prioridade: string): string {
    switch (prioridade) {
      case 'alta': return 'bg-red-200 text-red-900';
      case 'media': return 'bg-yellow-200 text-yellow-900';
      case 'baixa': return 'bg-green-200 text-green-900';
      default: return 'bg-gray-200 text-gray-900';
    }
  }

  onNextStepClick(step: NextStep): void {
    // Navegação baseada na URL do step
    if (step.url.startsWith('http')) {
      window.open(step.url, '_blank');
    } else {
      this.router.navigate([step.url]);
    }
  }

  onQuickAction(action: string): void {
    // TASK-ARCH003: Migrar Dashboard PDI - Ações rápidas implementadas
    switch (action) {
      case 'update-pdi':
        this.router.navigate(['/pdi/update']);
        break;
      case 'schedule-session':
        this.router.navigate(['/sessions/schedule']);
        break;
      case 'edit-profile':
        this.router.navigate(['/profile/edit']);
        break;
      case 'view-reports':
        this.router.navigate(['/reports']);
        break;
    }
  }
}
