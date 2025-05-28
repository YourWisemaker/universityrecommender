'use client';

import React, { useState, useEffect } from 'react';
import { ChevronDownIcon } from '@heroicons/react/24/outline';

interface DropdownOption {
  value: string;
  label: string;
}

interface DynamicDropdownProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  apiEndpoint?: string;
  staticOptions?: DropdownOption[];
  placeholder?: string;
  required?: boolean;
  className?: string;
  transformData?: (data: any) => DropdownOption[];
}

const DynamicDropdown: React.FC<DynamicDropdownProps> = ({
  label,
  value,
  onChange,
  apiEndpoint,
  staticOptions = [],
  placeholder = 'Select an option',
  required = false,
  className = '',
  transformData
}) => {
  const [options, setOptions] = useState<DropdownOption[]>(staticOptions);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (apiEndpoint) {
      fetchOptions();
    }
  }, [apiEndpoint]);

  const fetchOptions = async () => {
    if (!apiEndpoint) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000${apiEndpoint}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch options: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      let transformedOptions: DropdownOption[];
      
      if (transformData) {
        transformedOptions = transformData(data);
      } else {
        // Default transformation - assume data is an array of strings or objects with value/label
        if (Array.isArray(data)) {
          transformedOptions = data.map(item => 
            typeof item === 'string' 
              ? { value: item, label: item }
              : { value: item.value || item.code || item.id, label: item.label || item.name || item.title }
          );
        } else {
          transformedOptions = [];
        }
      }
      
      setOptions(transformedOptions);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch options');
      console.error('Error fetching dropdown options:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (selectedValue: string) => {
    onChange(selectedValue);
    setIsOpen(false);
  };

  const selectedOption = options.find(option => option.value === value);

  return (
    <div className={`relative ${className}`}>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="w-full h-10 px-3 py-2 text-left bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-gray-400 transition-colors flex items-center justify-between"
          disabled={loading}
        >
          <span className={selectedOption ? 'text-gray-900' : 'text-gray-500'}>
            {loading ? 'Loading...' : (selectedOption?.label || placeholder)}
          </span>
          <ChevronDownIcon 
            className={`h-4 w-4 text-gray-400 transition-transform ${
              isOpen ? 'rotate-180' : ''
            }`} 
          />
        </button>
        
        {isOpen && (
          <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
            {error ? (
              <div className="px-4 py-3 text-red-600 text-sm">
                {error}
                <button 
                  onClick={fetchOptions}
                  className="ml-2 text-blue-600 hover:text-blue-800 underline"
                >
                  Retry
                </button>
              </div>
            ) : options.length === 0 && !loading ? (
              <div className="px-4 py-3 text-gray-500 text-sm">
                No options available
              </div>
            ) : (
              options.map((option, index) => (
                <button
                  key={`${option.value}-${index}`}
                  onClick={() => handleSelect(option.value)}
                  className={`w-full px-4 py-3 text-left hover:bg-gray-50 focus:outline-none focus:bg-gray-50 transition-colors ${
                    option.value === value ? 'bg-blue-50 text-blue-700' : 'text-gray-900'
                  }`}
                >
                  {option.label}
                </button>
              ))
            )}
          </div>
        )}
      </div>
      
      {/* Click outside to close */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-40" 
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default DynamicDropdown;