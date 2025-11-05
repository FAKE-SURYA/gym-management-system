import api from './api'

const paymentService = {
  createOrder: async (membershipId) => {
    const response = await api.post('/payments/create-order', { membership_id: membershipId })
    return response.data
  },

  verifyPayment: async (paymentData) => {
    const response = await api.post('/payments/verify-payment', paymentData)
    return response.data
  },

  getPayments: async (memberId = null) => {
    let url = '/payments/'
    if (memberId) url += `?member_id=${memberId}`
    
    const response = await api.get(url)
    return response.data
  }
}

export default paymentService
