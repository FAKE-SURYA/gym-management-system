import api from './api'

const membershipService = {
  getAllMemberships: async (memberId = null, status = null) => {
    let url = '/memberships/'
    const params = new URLSearchParams()
    if (memberId) params.append('member_id', memberId)
    if (status) params.append('status', status)
    
    if (params.toString()) url += '?' + params.toString()
    
    const response = await api.get(url)
    return response.data
  },

  getMembership: async (membershipId) => {
    const response = await api.get(`/memberships/${membershipId}`)
    return response.data
  },

  createMembership: async (data) => {
    const response = await api.post('/memberships/', data)
    return response.data
  },

  getExpiringMemberships: async (days = 7) => {
    const response = await api.get(`/memberships/expiring/soon?days=${days}`)
    return response.data
  }
}

export default membershipService
