import React, { useState, useEffect } from 'react'
import membershipService from '../../services/membershipService'

const ExpiringMembers = () => {
  const [expiring, setExpiring] = useState([])

  useEffect(() => {
    fetchExpiringMemberships()
  }, [])

  const fetchExpiringMemberships = async () => {
    try {
      const data = await membershipService.getExpiringMemberships(7)
      setExpiring(data)
    } catch (error) {
      console.error('Error fetching expiring memberships:', error)
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Expiring Soon (7 Days)</h2>
      <div className="space-y-2">
        {expiring.length > 0 ? (
          expiring.map((membership) => (
            <div key={membership.id} className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm font-semibold">Member #{membership.member_id}</p>
              <p className="text-xs text-gray-600">Expires: {membership.end_date}</p>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-center py-4">No memberships expiring soon</p>
        )}
      </div>
    </div>
  )
}

export default ExpiringMembers
