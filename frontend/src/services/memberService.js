import api from './api'

const memberService = {
  getAllMembers: async (skip = 0, limit = 100) => {
    const response = await api.get(`/members/?skip=${skip}&limit=${limit}`)
    return response.data
  },

  getMember: async (memberId) => {
    const response = await api.get(`/members/${memberId}`)
    return response.data
  },

  updateMember: async (memberId, data) => {
    const response = await api.put(`/members/${memberId}`, data)
    return response.data
  },

  deleteMember: async (memberId) => {
    await api.delete(`/members/${memberId}`)
  }
}

export default memberService
