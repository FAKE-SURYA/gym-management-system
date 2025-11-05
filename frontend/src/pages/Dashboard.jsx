import React, { useState, useEffect } from 'react'
import Navbar from '../components/common/Navbar'
import StatsCard from '../components/dashboard/StatsCard'
import RevenueChart from '../components/dashboard/RevenueChart'
import ExpiringMembers from '../components/dashboard/ExpiringMembers'
import dashboardService from '../services/dashboardService'
import LoadingSpinner from '../components/common/LoadingSpinner'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await dashboardService.getStats()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Admin Dashboard</h1>
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard 
            title="Active Members" 
            value={stats?.active_members || 0} 
            icon="👥"
            bgColor="bg-blue-500"
          />
          <StatsCard 
            title="Expiring Soon" 
            value={stats?.expiring_soon || 0} 
            icon="⚠️"
            bgColor="bg-yellow-500"
          />
          <StatsCard 
            title="Monthly Revenue" 
            value={`₹${(stats?.monthly_revenue || 0).toLocaleString()}`} 
            icon="💰"
            bgColor="bg-green-500"
          />
          <StatsCard 
            title="Today's Attendance" 
            value={stats?.today_attendance || 0} 
            icon="✅"
            bgColor="bg-purple-500"
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <RevenueChart data={stats?.revenue_trend || []} />
          </div>
          <ExpiringMembers />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
