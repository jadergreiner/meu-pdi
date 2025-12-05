import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { signal } from '@angular/core';

import { UserStatisticsComponent } from './user-statistics.component';

// Mock do HttpClient para testes
describe('UserStatisticsComponent', () => {
  let component: UserStatisticsComponent;
  let fixture: ComponentFixture<UserStatisticsComponent>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        UserStatisticsComponent,
        HttpClientTestingModule
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserStatisticsComponent);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);
    fixture.detectChanges();
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with loading state', () => {
    expect(component.isLoading()).toBeTruthy();
    expect(component.error()).toBeFalsy();
    expect(component.statistics()).toBeFalsy();
  });

  it('should load statistics on init', () => {
    const mockStats = {
      dias_ativos: 15,
      objetivos_completados: 8,
      progresso_mensal: 75.5,
      sessoes_realizadas: 12,
      horas_dedicadas: 45.5,
      streak_atual: 7,
      nivel_engajamento: 'alto' as const,
      ultima_atividade: '2024-01-15T10:30:00Z'
    };

    const req = httpMock.expectOne('/api/users/statistics');
    expect(req.request.method).toBe('GET');
    req.flush(mockStats);

    expect(component.isLoading()).toBeFalsy();
    expect(component.error()).toBeFalsy();
    expect(component.statistics()).toEqual(mockStats);
  });

  it('should handle error response', () => {
    const errorMessage = 'Erro ao carregar estatísticas';

    const req = httpMock.expectOne('/api/users/statistics');
    expect(req.request.method).toBe('GET');
    req.flush(errorMessage, { status: 500, statusText: 'Internal Server Error' });

    expect(component.isLoading()).toBeFalsy();
    expect(component.error()).toBeTruthy();
    expect(component.statistics()).toBeFalsy();
  });

  it('should retry on error', () => {
    // Primeiro erro
    const req1 = httpMock.expectOne('/api/users/statistics');
    req1.flush('Error', { status: 500, statusText: 'Internal Server Error' });

    expect(component.error()).toBeTruthy();

    // Retry
    component.onRetry();

    const mockStats = {
      dias_ativos: 10,
      objetivos_completados: 5,
      progresso_mensal: 50.0,
      sessoes_realizadas: 8,
      horas_dedicadas: 30.0,
      streak_atual: 3,
      nivel_engajamento: 'medio' as const,
      ultima_atividade: '2024-01-10T09:00:00Z'
    };

    const req2 = httpMock.expectOne('/api/users/statistics');
    expect(req2.request.method).toBe('GET');
    req2.flush(mockStats);

    expect(component.isLoading()).toBeFalsy();
    expect(component.error()).toBeFalsy();
    expect(component.statistics()).toEqual(mockStats);
  });

  it('should compute engagement color correctly', () => {
    component.statistics.set({
      dias_ativos: 10,
      objetivos_completados: 5,
      progresso_mensal: 50.0,
      sessoes_realizadas: 8,
      horas_dedicadas: 30.0,
      streak_atual: 3,
      nivel_engajamento: 'alto',
      ultima_atividade: '2024-01-10T09:00:00Z'
    });

    expect(component.engagementColor()).toBe('alto');

    component.statistics.set({
      ...component.statistics()!,
      nivel_engajamento: 'medio'
    });

    expect(component.engagementColor()).toBe('medio');

    component.statistics.set({
      ...component.statistics()!,
      nivel_engajamento: 'baixo'
    });

    expect(component.engagementColor()).toBe('baixo');
  });

  it('should compute engagement icon correctly', () => {
    component.statistics.set({
      dias_ativos: 10,
      objetivos_completados: 5,
      progresso_mensal: 50.0,
      sessoes_realizadas: 8,
      horas_dedicadas: 30.0,
      streak_atual: 3,
      nivel_engajamento: 'alto',
      ultima_atividade: '2024-01-10T09:00:00Z'
    });

    expect(component.engagementIcon()).toBe('trending_up');

    component.statistics.set({
      ...component.statistics()!,
      nivel_engajamento: 'medio'
    });

    expect(component.engagementIcon()).toBe('trending_flat');

    component.statistics.set({
      ...component.statistics()!,
      nivel_engajamento: 'baixo'
    });

    expect(component.engagementIcon()).toBe('trending_down');
  });

  it('should handle empty statistics gracefully', () => {
    component.statistics.set(null);
    expect(component.engagementColor()).toBe('');
    expect(component.engagementIcon()).toBe('');
  });
});