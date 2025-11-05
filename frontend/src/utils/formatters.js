export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR'
  }).format(amount)
}

export const formatPhoneNumber = (phone) => {
  if (!phone) return 'N/A'
  return phone.replace(/(\d{2})(\d{5})(\d{5})/, '$1 $2 $3')
}
