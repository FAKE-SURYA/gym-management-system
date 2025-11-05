import React from 'react'

const StatsCard = ({ title, value, icon, bgColor }) => {
  return (
    <div className={`${bgColor} text-white p-6 rounded-lg shadow-lg`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm opacity-80">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className="text-4xl">{icon}</div>
      </div>
    </div>
  )
}

export default StatsCard
