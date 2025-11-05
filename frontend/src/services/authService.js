import api from './api'

const authService = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password })
    return response.data
  },

  register: async (email, password, full_name, phone = null, role = 'member') => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name,
      phone,
      role
    })
    return response.data
  },

  refresh: async (refreshToken) => {
    const response = await api.post('/auth/refresh', { refresh_token: refreshToken })
    return response.data
  }
}

export default authService
