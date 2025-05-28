"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import DynamicDropdown from "@/components/DynamicDropdown"
import {
  Upload,
  GraduationCap,
  MapPin,
  DollarSign,
  BookOpen,
  Briefcase,
  FileText,
  Globe,
  Calendar,
  Users,
  Star,
  Award,
  Clock,
  ExternalLink,
  Loader2,
  CheckCircle,
  AlertCircle,
  Info
} from "lucide-react"

interface FormData {
  cv: File | null
  degreeLevel: string
  fieldOfInterest: string
  gpa: string
  testScores: string
  preferredContinent: string
  preferredCountry: string
  budgetPreference: string
  researchInterests: string
  languagePreference: string
  targetStartYear: string
  studyMode: string
  careerGoal: string
}

interface University {
  id: number
  name: string
  country: string
  ranking: number
  matchScore: number
  tuitionFee: string
  scholarshipAvailable: boolean
  programName: string
  duration: string
  requirements: string[]
  researchAreas: string[]
  facultyHighlights: string[]
  campusLife: string
  applicationDeadline: string
  website: string
  description: string
  strengths: string[]
  admissionRate: string
}

// Mock data removed - application now uses only real API data

export default function UniversityRecommender() {
  const [formData, setFormData] = useState<FormData>({
    cv: null,
    degreeLevel: "",
    fieldOfInterest: "",
    gpa: "",
    testScores: "",
    preferredContinent: "",
    preferredCountry: "no-preference",
    budgetPreference: "",
    researchInterests: "",
    languagePreference: "",
    targetStartYear: "",
    studyMode: "",
    careerGoal: "",
  })

  const [recommendations, setRecommendations] = useState<University[]>([])
  const [aiSummary, setAiSummary] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [showResults, setShowResults] = useState(false)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    setFormData((prev) => ({ ...prev, cv: file }))
  }

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
  }

  const generateRecommendations = async () => {
    setIsLoading(true)

    try {
      // Prepare the student profile data for the API
      const studentProfile = {
        degree_level: formData.degreeLevel,
        field_of_interest: formData.fieldOfInterest,
        gpa: formData.gpa,
        test_scores: formData.testScores,
        preferred_continent: formData.preferredContinent,
        preferred_country: formData.preferredCountry,
        budget_preference: formData.budgetPreference,
        research_interests: formData.researchInterests,
        work_experience: "",
        language_preference: formData.languagePreference,
        target_start_year: formData.targetStartYear,
        study_mode: formData.studyMode,
        career_goal: formData.careerGoal
      }

      // Call the backend API
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentProfile)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      // Transform the API response to match frontend expectations (snake_case to camelCase)
      const transformedUniversities = (data.universities || []).map((uni: any) => ({
        ...uni,
        matchScore: uni.match_score,
        tuitionFee: uni.tuition_fee,
        admissionRate: uni.admission_rate,
        programName: uni.program_name,
        scholarshipAvailable: uni.scholarship_available,
        researchAreas: uni.research_areas,
        facultyHighlights: uni.faculty_highlights,
        campusLife: uni.campus_life,
        applicationDeadline: uni.application_deadline
      }))
      
      // Set the recommendations and AI summary from the API response
      setRecommendations(transformedUniversities)
      setAiSummary(data.ai_summary || 'No analysis available')
      setShowResults(true)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
      
      // Show error message to user without fallback to mock data
      setRecommendations([])
      setAiSummary('Unable to generate recommendations. Please check your internet connection and try again.')
      setShowResults(false)
      
      // Show error message to user
      alert('Unable to connect to recommendation service. Please check your connection and try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const resetForm = () => {
    setFormData({
      cv: null,
      degreeLevel: "",
      fieldOfInterest: "",
      gpa: "",
      testScores: "",
      preferredContinent: "",
      preferredCountry: "",
      budgetPreference: "",
      researchInterests: "",
      languagePreference: "",
      targetStartYear: "",
      studyMode: "",
      careerGoal: "",
    })
    setShowResults(false)
    setRecommendations([])
    setAiSummary("")
  }

  if (showResults) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-6xl mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                  <GraduationCap className="h-8 w-8 text-blue-600" />
                  University Recommendations
                </h1>
                <p className="text-gray-600 mt-1">AI-powered recommendations based on your academic profile</p>
              </div>
              <Button
                onClick={resetForm}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-medium"
              >
                New Search
              </Button>
            </div>
          </div>
        </div>

        <div className="max-w-6xl mx-auto px-4 py-8">
          {/* University Recommendations Table */}
          <Card className="mb-8 bg-white border border-gray-200 shadow-sm">
            <CardHeader className="bg-blue-50 border-b border-gray-200">
              <CardTitle className="text-xl text-gray-900 flex items-center gap-2">
                <Star className="h-5 w-5 text-blue-600" />
                Top 3 University Recommendations
              </CardTitle>
              <CardDescription className="text-gray-600">
                Universities ranked by compatibility with your academic profile
              </CardDescription>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50">
                    <TableHead className="font-semibold text-gray-900">University</TableHead>
                    <TableHead className="font-semibold text-gray-900">Program</TableHead>
                    <TableHead className="font-semibold text-gray-900">Match Score</TableHead>
                    <TableHead className="font-semibold text-gray-900">Details</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {recommendations && recommendations.map((uni, index) => (
                    <TableRow key={uni.id} className="hover:bg-gray-50">
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                              index === 0 ? "bg-yellow-500" : index === 1 ? "bg-gray-400" : "bg-orange-500"
                            }`}
                          >
                            {index + 1}
                          </div>
                          <div>
                            <div className="font-semibold text-gray-900">{uni.name}</div>
                            <div className="text-sm text-gray-600 flex items-center gap-1">
                              <MapPin className="h-3 w-3" />
                              {uni.country}
                            </div>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div>
                          <div className="font-medium text-gray-900">{uni.programName}</div>
                          <div className="text-sm text-gray-600">{uni.duration}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge
                          className={`${
                            index === 0
                              ? "bg-green-100 text-green-800"
                              : index === 1
                                ? "bg-blue-100 text-blue-800"
                                : "bg-purple-100 text-purple-800"
                          } font-semibold`}
                        >
                          {uni.matchScore}% Match
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
                              View Details
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                            <DialogHeader>
                              <DialogTitle className="text-2xl flex items-center gap-2">
                                <GraduationCap className="h-6 w-6 text-blue-600" />
                                {uni.name}
                              </DialogTitle>
                              <DialogDescription className="text-lg">
                                {uni.programName} • {uni.country}
                              </DialogDescription>
                            </DialogHeader>

                            <div className="space-y-6 mt-6">
                              {/* Overview */}
                              <div className="bg-blue-50 rounded-lg p-4">
                                <h4 className="font-semibold text-lg mb-2 text-blue-900">Program Overview</h4>
                                <p className="text-gray-700 mb-3">{uni.description}</p>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                  <div>
                                    <span className="font-medium">Duration:</span> {uni.duration}
                                  </div>
                                  <div>
                                    <span className="font-medium">Tuition:</span> {uni.tuitionFee}
                                  </div>
                                  <div>
                                    <span className="font-medium">Global Ranking:</span> #{uni.ranking}
                                  </div>
                                  <div>
                                    <span className="font-medium">Admission Rate:</span> {uni.admissionRate}
                                  </div>
                                </div>
                              </div>

                              {/* Requirements */}
                              <div>
                                <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                                  <FileText className="h-5 w-5 text-blue-600" />
                                  Admission Requirements
                                </h4>
                                <div className="flex flex-wrap gap-2">
                                  {uni.requirements && uni.requirements.map((req, idx) => (
                                    <Badge key={idx} variant="outline" className="border-blue-200 text-blue-800">
                                      {req}
                                    </Badge>
                                  ))}
                                </div>
                              </div>

                              {/* Research Areas */}
                              <div>
                                <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                                  <BookOpen className="h-5 w-5 text-blue-600" />
                                  Research Areas
                                </h4>
                                <div className="flex flex-wrap gap-2">
                                  {uni.researchAreas && uni.researchAreas.map((area, idx) => (
                                    <Badge key={idx} className="bg-blue-100 text-blue-800">
                                      {area}
                                    </Badge>
                                  ))}
                                </div>
                              </div>

                              {/* Faculty */}
                              <div>
                                <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                                  <Users className="h-5 w-5 text-blue-600" />
                                  Notable Faculty
                                </h4>
                                <ul className="space-y-1">
                                  {uni.facultyHighlights && uni.facultyHighlights.map((faculty, idx) => (
                                    <li key={idx} className="text-gray-700">
                                      • {faculty}
                                    </li>
                                  ))}
                                </ul>
                              </div>

                              {/* Strengths */}
                              <div>
                                <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                                  <Award className="h-5 w-5 text-blue-600" />
                                  Program Strengths
                                </h4>
                                <div className="flex flex-wrap gap-2">
                                  {uni.strengths && uni.strengths.map((strength, idx) => (
                                    <Badge key={idx} className="bg-green-100 text-green-800">
                                      {strength}
                                    </Badge>
                                  ))}
                                </div>
                              </div>

                              {/* Campus Life */}
                              <div>
                                <h4 className="font-semibold text-lg mb-3 flex items-center gap-2">
                                  <Globe className="h-5 w-5 text-blue-600" />
                                  Campus & Location
                                </h4>
                                <p className="text-gray-700">{uni.campusLife}</p>
                              </div>

                              {/* Application Info */}
                              <div className="bg-gray-50 rounded-lg p-4">
                                <div className="flex justify-between items-center">
                                  <div>
                                    <h4 className="font-semibold flex items-center gap-2">
                                      <Clock className="h-4 w-4 text-blue-600" />
                                      Application Deadline
                                    </h4>
                                    <p className="text-gray-600">{uni.applicationDeadline}</p>
                                  </div>
                                  <Button asChild className="bg-blue-600 hover:bg-blue-700 text-white">
                                    <a href={uni.website} target="_blank" rel="noopener noreferrer">
                                      <ExternalLink className="mr-2 h-4 w-4" />
                                      Visit Website
                                    </a>
                                  </Button>
                                </div>
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          {/* AI Summary */}
          <Card className="bg-white border border-gray-200 shadow-sm">
            <CardHeader className="bg-blue-50 border-b border-gray-200">
              <CardTitle className="text-xl text-gray-900 flex items-center gap-2">
                <Briefcase className="h-5 w-5 text-blue-600" />
                AI Analysis & Recommendations
              </CardTitle>
              <CardDescription className="text-gray-600">
                Comprehensive analysis of your profile and personalized recommendations
              </CardDescription>
            </CardHeader>
            <CardContent className="p-6">
              <div className="prose max-w-none">
                {aiSummary.split("\n\n").map((paragraph, index) => (
                  <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                    {paragraph.split("**").map((part, partIndex) =>
                      partIndex % 2 === 1 ? (
                        <strong key={partIndex} className="font-semibold text-blue-900">
                          {part}
                        </strong>
                      ) : (
                        part
                      ),
                    )}
                  </p>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center gap-3">
            <GraduationCap className="h-10 w-10 text-blue-600" />
            University Recommender
          </h1>
          <p className="text-xl text-gray-600 mb-2">AI-powered university matching for your academic journey</p>
          <p className="text-gray-500">Get personalized recommendations based on your profile and preferences</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card className="bg-white border border-gray-200 shadow-sm">
          <CardHeader className="bg-blue-50 border-b border-gray-200">
            <CardTitle className="text-2xl text-gray-900 flex items-center gap-2">
              <Users className="h-6 w-6 text-blue-600" />
              Academic Profile Assessment
            </CardTitle>
            <CardDescription className="text-gray-600 text-lg">
              Provide your information to receive tailored university recommendations
            </CardDescription>
          </CardHeader>
          <CardContent className="p-6 space-y-8">
            {/* CV Upload */}
            <div className="bg-blue-50 rounded-lg p-6 border border-blue-100">
              <Label htmlFor="cv" className="text-gray-900 font-semibold text-lg flex items-center gap-2 mb-3">
                <FileText className="h-5 w-5 text-blue-600" />
                Academic CV/Resume
              </Label>
              <p className="text-gray-600 text-sm mb-4">Upload your academic CV or resume (PDF, DOC, DOCX)</p>
              <div className="relative">
                <input
                  id="cv"
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileUpload}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                />
                <div className="flex items-center gap-3 p-3 bg-white border border-gray-300 rounded-lg hover:border-blue-400 transition-colors">
                  <Button
                    type="button"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium pointer-events-none"
                  >
                    <Upload className="mr-2 h-4 w-4" />
                    Choose File
                  </Button>
                  <span className="text-gray-600">{formData.cv ? formData.cv.name : "No file chosen"}</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Degree Level */}
              <div>
                <Label htmlFor="degree" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <GraduationCap className="h-4 w-4 text-blue-600" />
                  Intended Degree Level
                </Label>
                <Select value={formData.degreeLevel} onValueChange={(value) => handleInputChange("degreeLevel", value)}>
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select degree level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="bachelors">Bachelor's</SelectItem>
                    <SelectItem value="masters">Master's</SelectItem>
                    <SelectItem value="phd">PhD</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Field of Interest */}
              <div>
                <DynamicDropdown
                  label="Field of Interest"
                  value={formData.fieldOfInterest}
                  onChange={(value) => handleInputChange("fieldOfInterest", value)}
                  apiEndpoint="/fields"
                  placeholder="Select field of study"
                  transformData={(data) => data.fields?.map((field: string) => ({ value: field, label: field })) || []}
                  className=""
                />
              </div>

              {/* GPA */}
              <div>
                <Label htmlFor="gpa" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Star className="h-4 w-4 text-blue-600" />
                  GPA
                </Label>
                <Input
                  id="gpa"
                  placeholder="e.g., 3.78/4.00"
                  value={formData.gpa}
                  onChange={(e) => handleInputChange("gpa", e.target.value)}
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>

              {/* Test Scores */}
              <div>
                <Label htmlFor="tests" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Award className="h-4 w-4 text-blue-600" />
                  Test Scores (Optional)
                </Label>
                <Input
                  id="tests"
                  placeholder="e.g., TOEFL 105, GRE 320"
                  value={formData.testScores}
                  onChange={(e) => handleInputChange("testScores", e.target.value)}
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                />
              </div>

              {/* Preferred Continent */}
              <div>
                <Label htmlFor="continent" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Globe className="h-4 w-4 text-blue-600" />
                  Preferred Continent
                </Label>
                <Select
                  value={formData.preferredContinent}
                  onValueChange={(value) => handleInputChange("preferredContinent", value)}
                >
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select continent" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="north-america">North America</SelectItem>
                    <SelectItem value="europe">Europe</SelectItem>
                    <SelectItem value="asia">Asia</SelectItem>
                    <SelectItem value="australia">Australia</SelectItem>
                    <SelectItem value="south-america">South America</SelectItem>
                    <SelectItem value="africa">Africa</SelectItem>
                    <SelectItem value="no-preference">No preference</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Preferred Country */}
              <div>
                <DynamicDropdown
                  label="Preferred Country"
                  value={formData.preferredCountry}
                  onChange={(value) => handleInputChange("preferredCountry", value)}
                  apiEndpoint="/countries"
                  placeholder="Select country"
                  transformData={(data) => {
                    const countries = data.countries?.map((country: any) => ({ 
                      value: country.code, 
                      label: country.name 
                    })) || [];
                    // Add "No preference" option
                    return [{ value: "no-preference", label: "No preference" }, ...countries];
                  }}
                  className=""
                />
              </div>

              {/* Budget Preference */}
              <div>
                <Label htmlFor="budget" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <DollarSign className="h-4 w-4 text-blue-600" />
                  Budget or Scholarship Preference
                </Label>
                <Select
                  value={formData.budgetPreference}
                  onValueChange={(value) => handleInputChange("budgetPreference", value)}
                >
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select funding preference" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="full-funding">Need full funding</SelectItem>
                    <SelectItem value="partial-funding">Partial funding acceptable</SelectItem>
                    <SelectItem value="self-funded">Self-funded</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Language Preference */}
              <div>
                <Label htmlFor="language" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Users className="h-4 w-4 text-blue-600" />
                  Language Preference
                </Label>
                <Select
                  value={formData.languagePreference}
                  onValueChange={(value) => handleInputChange("languagePreference", value)}
                >
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select language preference" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="english-only">English only</SelectItem>
                    <SelectItem value="multilingual">Multilingual programs OK</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Target Start Year */}
              <div>
                <Label htmlFor="year" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Calendar className="h-4 w-4 text-blue-600" />
                  Target Start Year
                </Label>
                <Select
                  value={formData.targetStartYear}
                  onValueChange={(value) => handleInputChange("targetStartYear", value)}
                >
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select start year" />
                  </SelectTrigger>
                  <SelectContent>
                    {Array.from({ length: 11 }, (_, i) => {
                      const year = new Date().getFullYear() + i;
                      return (
                        <SelectItem key={year} value={year.toString()}>
                          {year}
                        </SelectItem>
                      );
                    })}
                  </SelectContent>
                </Select>
              </div>

              {/* Study Mode */}
              <div>
                <Label htmlFor="mode" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <BookOpen className="h-4 w-4 text-blue-600" />
                  Mode of Study
                </Label>
                <Select value={formData.studyMode} onValueChange={(value) => handleInputChange("studyMode", value)}>
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select study mode" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="on-campus">On-campus</SelectItem>
                    <SelectItem value="online">Online</SelectItem>
                    <SelectItem value="hybrid">Hybrid</SelectItem>
                    <SelectItem value="no-preference">No preference</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Career Goal */}
              <div>
                <Label htmlFor="career" className="text-gray-900 font-medium flex items-center gap-2 mb-2">
                  <Briefcase className="h-4 w-4 text-blue-600" />
                  Career Goal
                </Label>
                <Select value={formData.careerGoal} onValueChange={(value) => handleInputChange("careerGoal", value)}>
                  <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500">
                    <SelectValue placeholder="Select career goal" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="industry">Industry</SelectItem>
                    <SelectItem value="academia">Academia</SelectItem>
                    <SelectItem value="research-labs">Research labs</SelectItem>
                    <SelectItem value="entrepreneurship">Entrepreneurship</SelectItem>
                    <SelectItem value="not-sure">Not sure yet</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Research Interests */}
            <div>
              <Label htmlFor="research" className="text-gray-900 font-medium text-lg flex items-center gap-2 mb-2">
                <BookOpen className="h-5 w-5 text-blue-600" />
                Research Interests
              </Label>
              <Textarea
                id="research"
                placeholder="e.g., AI for healthcare, Ethical AI, Low-resource NLP"
                value={formData.researchInterests}
                onChange={(e) => handleInputChange("researchInterests", e.target.value)}
                rows={3}
                className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 resize-none"
              />
            </div>



            <Button
              onClick={generateRecommendations}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 text-lg font-semibold rounded-lg shadow-sm"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <div className="mr-3 h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  Analyzing Your Profile...
                </>
              ) : (
                <>
                  <GraduationCap className="mr-3 h-5 w-5" />
                  Get My University Recommendations
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
