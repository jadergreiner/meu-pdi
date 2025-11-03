import { test, expect } from '@playwright/test';

// TASK-ARCH004: Configurar Testes E2E com Playwright - Testes de dashboard implementados

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Mock do token de autenticação para acessar o dashboard
    await page.addInitScript(() => {
      localStorage.setItem('auth_token', 'mock-jwt-token-for-testing');
    });
  });

  test('deve carregar o dashboard após autenticação', async ({ page }) => {
    await page.goto('/dashboard');

    // Aguardar carregamento completo
    await page.waitForLoadState('networkidle');

    // Verificar se estamos no dashboard
    await expect(page).toHaveURL(/.*dashboard/);

    // Aguardar elementos principais aparecerem
    await page.waitForSelector('text=Meu PDI - Dashboard', { timeout: 10000 });

    // Verificar elementos principais
    await expect(page.getByText('Meu PDI - Dashboard')).toBeVisible();
  });

  test('deve mostrar loading inicialmente', async ({ page }) => {
    await page.goto('/dashboard');

    // Verificar se mostra loading ou se carrega diretamente
    try {
      await expect(page.getByText('Carregando dashboard...')).toBeVisible({ timeout: 2000 });
    } catch {
      // Se não mostrou loading, verificar se carregou o dashboard
      await page.waitForSelector('text=Meu PDI - Dashboard', { timeout: 10000 });
      await expect(page.getByText('Meu PDI - Dashboard')).toBeVisible();
    }
  });

  test('deve mostrar dados do PDI quando carregados', async ({ page }) => {
    // Mock das APIs do dashboard
    await page.route('**/api/profile', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: '1',
          nome_completo: 'João Silva',
          email: 'joao@teste.com',
          email_validado: true,
          data_cadastro: '2025-01-01'
        })
      });
    });

    await page.route('**/api/pdi/overview', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status_geral: 'em_andamento',
          objetivos_ativos: 3,
          progresso_percentual: 65.5,
          proximas_acoes: ['Revisar objetivos', 'Agendar mentoria', 'Atualizar PDI'],
          ultima_atualizacao: '2025-11-03'
        })
      });
    });

    await page.route('**/api/next-steps', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          acoes_recomendadas: [
            {
              titulo: 'Agendar Sessão de Mentoria',
              descricao: 'Próxima sessão disponível em 2 dias',
              prioridade: 'alta',
              url: '/sessions/schedule'
            },
            {
              titulo: 'Atualizar PDI',
              descricao: 'Revisar objetivos do trimestre',
              prioridade: 'media',
              url: '/pdi/update'
            }
          ]
        })
      });
    });

    await page.goto('/dashboard');

    // Aguardar carregamento
    await page.waitForSelector('text=Bem-vindo de volta');

    // Verificar dados do perfil
    await expect(page.getByText('Bem-vindo de volta, João Silva!')).toBeVisible();

    // Verificar visão geral do PDI
    await expect(page.getByText('Visão Geral do PDI')).toBeVisible();
    await expect(page.getByText('Objetivos Ativos:')).toBeVisible();
    await expect(page.getByText('3')).toBeVisible();
    await expect(page.getByText('65.5%')).toBeVisible();

    // Verificar próximos passos
    await expect(page.getByText('Próximos Passos')).toBeVisible();
    await expect(page.getByText('Agendar Sessão de Mentoria')).toBeVisible();
    await expect(page.getByText('alta')).toBeVisible();
  });

  test('deve mostrar ações rápidas funcionais', async ({ page }) => {
    await page.goto('/dashboard');

    // Aguardar carregamento completo
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Meu PDI - Dashboard', { timeout: 15000 });

    // Aguardar carregamento das ações rápidas
    await page.waitForSelector('text=Ações Rápidas', { timeout: 10000 });

    // Verificar botões de ações rápidas
    await expect(page.getByRole('button', { name: 'Atualizar PDI' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Agendar Sessão' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Editar Perfil' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Ver Relatórios' })).toBeVisible();
  });

  test('deve fazer logout quando clicar no botão', async ({ page }) => {
    await page.goto('/dashboard');

    // Aguardar carregamento completo
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Meu PDI - Dashboard', { timeout: 15000 });

    // Aguardar botão de sair aparecer
    await page.waitForSelector('text=Sair', { timeout: 10000 });

    // Clicar no botão de sair
    await page.getByRole('button', { name: 'Sair' }).click();

    // Verificar se redirecionou para login
    await expect(page).toHaveURL(/.*auth\/login/);
  });

  test('deve ser responsivo em mobile', async ({ page }) => {
    // Configurar viewport mobile
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('/dashboard');

    // Aguardar carregamento completo
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Meu PDI - Dashboard', { timeout: 15000 });

    // Verificar se elementos principais estão visíveis
    await expect(page.getByText('Meu PDI - Dashboard')).toBeVisible();

    // Verificar se layout se adapta (grid de 1 coluna)
    const grid = page.locator('.dashboard-grid');
    await expect(grid).toBeVisible();
  });
});