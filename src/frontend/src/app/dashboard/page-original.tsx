'use client'

import { useState, useEffect } from 'react'

interface UserProfile {
  id: string
  nome_completo: string
  email: string
  email_validado: boolean
  data_cadastro: string
}

interface PDIOverview {
  status_geral: string
  objetivos_ativos: number
  progresso_percentual: number
  proximas_acoes: string[]
  ultima_atualizacao: string
}

interface NextStep {
  titulo: string
  descricao: string
  prioridade: 'alta' | 'media' | 'baixa'
  url: string
}

export default function Dashboard() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [pdiOverview, setPdiOverview] = useState<PDIOverview | null>(null)
  const [nextSteps, setNextSteps] = useState<NextStep[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        // Verificar se há token
        const token = localStorage.getItem('access_token')
        if (!token) {
          window.location.href = '/auth/login'
          return
        }

        const headers = {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }

        // Buscar dados do perfil
        const profileResponse = await fetch('http://localhost:8000/profile', { headers })
        if (profileResponse.ok) {
          const profileData = await profileResponse.json()
          setProfile(profileData)
        }

        // Buscar visão geral do PDI
        const pdiResponse = await fetch('http://localhost:8000/pdi/overview', { headers })
        if (pdiResponse.ok) {
          const pdiData = await pdiResponse.json()
          setPdiOverview(pdiData)
        }

        // Buscar próximos passos
        const nextStepsResponse = await fetch('http://localhost:8000/next-steps', { headers })
        if (nextStepsResponse.ok) {
          const nextStepsData = await nextStepsResponse.json()
          setNextSteps(nextStepsData.acoes_recomendadas || [])
        }

      } catch (err) {
        setError('Erro ao carregar dados do dashboard')
        console.error('Dashboard error:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    window.location.href = '/'
  }

  const getPriorityColor = (prioridade: string) => {
    switch (prioridade) {
      case 'alta': return 'bg-red-100 text-red-800 border-red-200'
      case 'media': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'baixa': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-xl sm:text-2xl font-bold text-gray-900">
              Meu PDI - Dashboard
            </h1>
            <div className="flex items-center space-x-4">
              {profile && (
                <span className="text-sm text-gray-600 hidden sm:block">
                  Olá, {profile.nome_completo.split(' ')[0]}!
                </span>
              )}
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-3 py-1 sm:px-4 sm:py-2 rounded text-sm hover:bg-red-700 transition-colors"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        {profile && (
          <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6 mb-8">
            <h2 className="text-lg sm:text-xl font-semibold text-gray-900 mb-2">
              Bem-vindo de volta, {profile.nome_completo}!
            </h2>
            <p className="text-gray-600 text-sm sm:text-base">
              Continue sua jornada de desenvolvimento pessoal. Aqui está seu progresso atual.
            </p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {/* PDI Overview */}
          <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Visão Geral do PDI
            </h3>
            {pdiOverview ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Status Geral:</span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    pdiOverview.status_geral === 'iniciando' ? 'bg-blue-100 text-blue-800' :
                    pdiOverview.status_geral === 'em_andamento' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {pdiOverview.status_geral.replace('_', ' ').toUpperCase()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600">Objetivos Ativos:</span>
                  <span className="font-semibold">{pdiOverview.objetivos_ativos}</span>
                </div>

                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-gray-600">Progresso Geral:</span>
                    <span className="font-semibold">{pdiOverview.progresso_percentual.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${Math.min(pdiOverview.progresso_percentual, 100)}%` }}
                    ></div>
                  </div>
                </div>

                {pdiOverview.proximas_acoes.length > 0 && (
                  <div>
                    <span className="text-sm text-gray-600 block mb-2">Próximas Ações:</span>
                    <ul className="text-sm text-gray-700 space-y-1">
                      {pdiOverview.proximas_acoes.slice(0, 3).map((acao, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-blue-500 mr-2">•</span>
                          {acao}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">Dados do PDI não disponíveis</p>
            )}
          </div>

          {/* Next Steps */}
          <div className="bg-white rounded-lg shadow-sm p-4 sm:p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Próximos Passos
            </h3>
            {nextSteps.length > 0 ? (
              <div className="space-y-3">
                {nextSteps.slice(0, 4).map((step, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border cursor-pointer hover:shadow-md transition-shadow ${
                      getPriorityColor(step.prioridade)
                    }`}
                    onClick={() => window.location.href = step.url}
                  >
                    <div className="flex justify-between items-start mb-1">
                      <h4 className="font-medium text-sm sm:text-base">{step.titulo}</h4>
                      <span className={`px-2 py-1 rounded text-xs font-medium capitalize ${
                        step.prioridade === 'alta' ? 'bg-red-200 text-red-900' :
                        step.prioridade === 'media' ? 'bg-yellow-200 text-yellow-900' :
                        'bg-green-200 text-green-900'
                      }`}>
                        {step.prioridade}
                      </span>
                    </div>
                    <p className="text-xs sm:text-sm opacity-80">{step.descricao}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">Nenhuma ação recomendada no momento</p>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow-sm p-4 sm:p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Ações Rápidas
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4">
            <button className="p-3 sm:p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors text-center">
              <div className="text-blue-600 text-lg sm:text-xl mb-1">📝</div>
              <div className="text-xs sm:text-sm font-medium text-blue-900">Atualizar PDI</div>
            </button>
            <button className="p-3 sm:p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors text-center">
              <div className="text-green-600 text-lg sm:text-xl mb-1">📅</div>
              <div className="text-xs sm:text-sm font-medium text-green-900">Agendar Sessão</div>
            </button>
            <button className="p-3 sm:p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors text-center">
              <div className="text-purple-600 text-lg sm:text-xl mb-1">👤</div>
              <div className="text-xs sm:text-sm font-medium text-purple-900">Editar Perfil</div>
            </button>
            <button className="p-3 sm:p-4 bg-orange-50 hover:bg-orange-100 rounded-lg transition-colors text-center">
              <div className="text-orange-600 text-lg sm:text-xl mb-1">📊</div>
              <div className="text-xs sm:text-sm font-medium text-orange-900">Ver Relatórios</div>
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}