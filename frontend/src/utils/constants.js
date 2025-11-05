export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const MEMBERSHIP_STATUS = {
  ACTIVE: 'active',
  EXPIRED: 'expired',
  SUSPENDED: 'suspended',
  CANCELLED: 'cancelled'
}

export const PAYMENT_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  FAILED: 'failed',
  REFUNDED: 'refunded'
}

export const USER_ROLES = {
  ADMIN: 'admin',
  TRAINER: 'trainer',
  MEMBER: 'member'
}
