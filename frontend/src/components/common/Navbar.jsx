import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const Navbar = () => {
  const { logout, user } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-8">
            <h1 className="text-2xl font-bold">💪 Gym Management</h1>
            <div className="hidden md:flex space-x-6">
              <Link to="/dashboard" className="hover:text-blue-200">Dashboard</Link>
              <Link to="/members" className="hover:text-blue-200">Members</Link>
              <Link to="/memberships" className="hover:text-blue-200">Memberships</Link>
              <Link to="/payments" className="hover:text-blue-200">Payments</Link>
              <Link to="/attendance" className="hover:text-blue-200">Attendance</Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm">👤 {user?.full_name}</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
