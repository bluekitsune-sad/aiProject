# Group Members:

Name: Saad Yousuf  
ID: 22639  
Email: Saad.g22639@iqra.edu.pk

Name: Ashad Tahir  
ID: 25255  
Email: Ashad.g25255@iqra.edu.pk

Name: Amna Siddiqui  
ID: 24949  
Email: Amna.g24949@iqra.edu.pk

# Bus Management System

A comprehensive web-based application for managing university bus routes, drivers, and students. The system features an interactive map interface for route visualization and real-time tracking, making it easier for administrators to manage transportation and for students to track their bus schedules.

## Project Video Representation:
   [Video Link](https://drive.google.com/file/d/1fvCIp7OuW0OD-d5U29HpvvEX0SVDXmi6/view?usp=sharing)

## Project Introduction

The Bus Management System is designed to streamline university transportation management by providing:

- **Real-time Route Visualization**: Interactive map interface showing bus routes and stops.
- **Multi-User Platform**: Separate dashboards for administrators, drivers, and students.
- **Route Management**: Easy assignment and modification of bus routes.
- **Class Schedule Integration**: Students can manage their class schedules in relation to bus timings.

### Key Components:

- **Frontend**: HTML5, CSS3, JavaScript, Leaflet.js for maps.
- **Backend**: Python Flask API.
- **Database**: MongoDB Atlas.
- **Map Services**: OpenStreetMap.

## Installation Guide

### Prerequisites

- Python 3.7+
- MongoDB Atlas account
- Internet connection (for maps and database)
- Modern web browser

### Step-by-Step Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd aiProject
   ```

2. Install the required packages:
   
   after runing the run.py all the required dependency will be downloaded

3. Set up the environment variables for MongoDB connection.

4. Start the backend server:

   ```bash
   python run.py
   ```

5. Open the application in your default browser.

## User Features

### Admin Dashboard

- **User Management**
  - Add/Edit/Delete drivers and students.
  - View all registered users.
- **Route Management**
  - Assign routes to drivers.
  - Set stop locations and timings.
  - Monitor all active routes.

### Driver Dashboard

- **Route Visualization**
  - View assigned routes on an interactive map.
  - See all stops and timings.
  - Get directions to each stop.
- **Schedule Management**
  - View daily schedule.
  - Check stop timings.

### Student Dashboard

- **Class Management**
  - Add/Edit class schedules.
  - View class timings.
- **Bus Schedule**
  - View available bus routes.
  - Check bus timings for classes.

## Future Enhancements

1. **Real-time Tracking**

   - GPS integration for live bus tracking.
   - ETA calculations for each stop.
   - Push notifications for delays.

2. **Advanced Route Planning**

   - Automatic route optimization.
   - Traffic-aware routing.
   - Multiple route suggestions.

3. **Mobile Application**

   - Native Android/iOS apps.
   - Push notifications.
   - Offline functionality.

4. **Enhanced Security**

   - Two-factor authentication.
   - Role-based access control.
   - Session management.

5. **Analytics Dashboard**

   - Route efficiency metrics.
   - Usage statistics.
   - Peak time analysis.

6. **Student Features**
   - Bus pass management.
   - Attendance tracking.
   - Feedback system.

## Project Structure

```
aiProject/
├── Backend/
│   └── app.py
├── Frontend/
│   ├── admin_dashboard.html
│   ├── driver_dashboard.html
│   ├── student_dashboard.html
│   └── login.html
├── run.py
└── README.md
```
