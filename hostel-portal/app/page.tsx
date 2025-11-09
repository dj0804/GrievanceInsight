import Image from "next/image";
import Link from "next/link";
import { FileText, Bot, BarChart3 } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Image
              src="/symbol.jpeg"
              alt="Logo"
              width={40}
              height={40}
              className="dark:invert"
              />
              <span className="text-xl font-bold text-gray-900">Dormify</span>
            </div>
            <nav className="flex space-x-6">
              <Link href="/submit" className="text-gray-600 hover:text-gray-900">
                Submit Grievance
              </Link>
              <Link href="/admin" className="text-gray-600 hover:text-gray-900">
                Admin Dashboard
              </Link>
              <Link href="/about" className="text-gray-600 hover:text-gray-900">
                About
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Hostel Grievance
            <span className="text-blue-600 block">Management System</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            AI-powered system for analyzing and managing hostel complaints. 
            Submit your grievances and get instant categorization, sentiment analysis, and priority assessment.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/submit"
              className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
            >
              Submit a Grievance
            </Link>
            <Link
              href="/admin"
              className="inline-flex items-center px-8 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
            >
              View Dashboard
            </Link>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Submit</h3>
              <p className="text-gray-600">
                Describe your hostel-related issue or concern in detail
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Bot className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyze</h3>
              <p className="text-gray-600">
                AI automatically categorizes, analyzes sentiment, and determines urgency
              </p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Track</h3>
              <p className="text-gray-600">
                Admins can view comprehensive dashboards and analytics
              </p>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div className="mt-20 bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">
            System Capabilities
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">100%</div>
              <div className="text-gray-600">Automated Processing</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">24/7</div>
              <div className="text-gray-600">System Availability</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">5+</div>
              <div className="text-gray-600">Complaint Categories</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-red-600 mb-2">Fast</div>
              <div className="text-gray-600">Response Time</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <Image
                src="/symbol.jpeg"
                alt="Logo"
                width={30}
                height={30}
                className="dark:invert"
              />
              <span className="text-lg font-semibold">Dormify</span>
            </div>
            <p className="text-gray-400">
              AI-powered grievance management for better hostel living
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}