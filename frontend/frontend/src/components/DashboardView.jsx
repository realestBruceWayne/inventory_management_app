import React from 'react';
import { Package, ShoppingCart, AlertCircle, TrendingUp, Users, Box } from 'lucide-react';

export default function DashboardView({ dashboard, products }) {
  const totalProducts = products.length;
  const lowStockCount = products.filter(p => p.quantity <= 5).length;

  const kpiCards = [
    {
      title: 'Total Products',
      value: dashboard?.total_products || totalProducts,
      icon: Package,
      gradient: 'from-blue-500 to-blue-600',
      textGradient: 'from-blue-600 to-purple-600',
      trend: '+12.5% from last month',
      trendColor: 'text-green-600',
    },
    {
      title: 'Total Customers',
      value: dashboard?.total_customers || 0,
      icon: Users,
      gradient: 'from-purple-500 to-purple-600',
      textGradient: 'from-purple-600 to-pink-600',
      trend: '+8.2% from last month',
      trendColor: 'text-green-600',
    },
    {
      title: 'Total Orders',
      value: dashboard?.total_orders || 0,
      icon: ShoppingCart,
      gradient: 'from-green-500 to-green-600',
      textGradient: 'from-green-600 to-teal-600',
      trend: '+23.1% from last month',
      trendColor: 'text-green-600',
    },
    {
      title: 'Low Stock Alerts',
      value: dashboard?.low_stock_count || lowStockCount,
      icon: AlertCircle,
      gradient: 'from-red-500 to-red-600',
      textGradient: 'from-red-600 to-orange-600',
      trend: 'Requires attention',
      trendColor: 'text-red-600',
      trendIcon: AlertCircle,
    },
  ];

  return (
    <>
      {/* KPI Dashboard Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {kpiCards.map((card, index) => {
          const Icon = card.icon;
          const TrendIcon = card.trendIcon || TrendingUp;
          return (
            <div
              key={index}
              className="bg-white/80 backdrop-blur-lg p-6 rounded-2xl border border-gray-200/50 shadow-lg hover:shadow-xl transition-all duration-300 group"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-500 mb-1">{card.title}</p>
                  <p className={`text-3xl font-bold bg-gradient-to-r ${card.textGradient} bg-clip-text text-transparent`}>
                    {card.value}
                  </p>
                </div>
                <div className={`bg-gradient-to-br ${card.gradient} p-4 rounded-xl shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className={`mt-4 flex items-center text-sm ${card.trendColor}`}>
                <TrendIcon className="h-4 w-4 mr-1" />
                <span>{card.trend}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Low Stock Products */}
      {dashboard?.low_stock_items && dashboard.low_stock_items.length > 0 && (
        <div className="bg-white/80 backdrop-blur-lg rounded-2xl border border-gray-200/50 shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
            Low Stock Products
          </h3>
          <div className="space-y-3">
            {dashboard.low_stock_items.map((product) => (
              <div
                key={product.id}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-red-50 to-orange-50 rounded-xl border border-red-100 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center gap-3">
                  <div className="bg-red-100 p-2 rounded-lg">
                    <Box className="h-5 w-5 text-red-600" />
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">{product.name}</p>
                    <p className="text-sm text-gray-500">SKU: {product.sku}</p>
                  </div>
                </div>
                <span className="bg-red-100 text-red-700 px-3 py-1 rounded-full text-sm font-semibold">
                  {product.quantity} units
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
