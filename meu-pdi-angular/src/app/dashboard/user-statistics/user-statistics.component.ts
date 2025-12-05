import { Component, OnInit, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Subject, takeUntil } from 'rxjs';

export interface UserStatistics {
  dias_ativos: number;
  objetivos_completados: number;
  progresso_mensal: number;
  sessoes_realizadas: number;
  horas_dedicadas: number;
  streak_atual: number;
  nivel_engajamento: 'baixo' | 'medio' | 'alto';
  ultima_atividade: string;
}

@Component({
  selector: 'app-user-statistics',
  templateUrl: './user-statistics.component.html',
  styleUrl: './user-statistics.component.scss'
})
export class UserStatisticsComponent implements OnInit {
  private destroy$ = new Subject<void>();

  // Signals para estado reativo
  isLoading = signal(true);
  error = signal<string | null>(null);
  statistics = signal<UserStatistics | null>(null);

  // Computed signals para métricas derivadas
  engagementColor = computed(() => {
    const stats = this.statistics();
    if (!stats) return 'gray';

    switch (stats.nivel_engajamento) {
      case 'alto': return 'green';
      case 'medio': return 'orange';
      case 'baixo': return 'red';
      default: return 'gray';
    }
  });

  engagementIcon = computed(() => {
    const stats = this.statistics();
    if (!stats) return 'help';

    switch (stats.nivel_engajamento) {
      case 'alto': return 'trending_up';
      case 'medio': return 'trending_flat';
      case 'baixo': return 'trending_down';
      default: return 'help';
    }
  });

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.loadStatistics();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  private loadStatistics(): void {
    this.isLoading.set(true);
    this.error.set(null);

    this.http.get<UserStatistics>('/api/users/statistics')
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (stats) => {
          this.statistics.set(stats);
          this.isLoading.set(false);
        },
        error: (err) => {
          console.error('Erro ao carregar estatísticas:', err);
          this.error.set('Erro ao carregar estatísticas. Tente novamente.');
          this.isLoading.set(false);
        }
      });
  }

  onRetry(): void {
    this.loadStatistics();
  }
}
