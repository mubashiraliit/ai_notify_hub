import React from 'react';
import '../css/admin_styles.css';
import colors from '../../theme/Color';
import images from '../../images/Image';

// Components
import AcademicNotices from '../components/AcademicNotices';
import DailyQuotes from '../components/DailyQuotes';
import ImportantAlerts from '../components/ImportantAlerts';

import DepartmentTimetables from '../components/DepartmentTimetables';
import ExamUpdates from '../components/ExamUpdates';
import StudentAchievements from '../components/StudentAchievements';
import StudentAIFAQs from '../components/StudentAIFAQs';

const AdminPanel = () => {
  return (
    <>
      <div id="container">
        {/* ---------- LEFT AREA ---------- */}
        <div id="logo_area_container">
          <div id="logo_area" style={{ backgroundColor: colors.light_grey }}>
            <img src={images.logo} className="logo_here" alt="logo here" />
            <div className="logo_name" style={{ color: colors.secondary }}>
              gc university hyderabad
            </div>
          </div>

          {/* Academic Notices Section */}
          <AcademicNotices />
        </div>

        {/* ---------- CENTER AREA ---------- */}
        <div className="center_area">
          <DailyQuotes />
          <ImportantAlerts />
          <DepartmentTimetables />
        </div>

        {/* ---------- RIGHT AREA ---------- */}
        <div className="third_area">
          <ExamUpdates />
          <StudentAchievements />
          <StudentAIFAQs />


        </div>
      </div>

      {/* ---------- FOOTER ---------- */}
      <div
        style={{
          backgroundColor: colors.secondary,
          color: colors.primary,
          textAlign: 'center',
          fontSize: 11,
          position: 'fixed',
          bottom: 0,
          left: 0,
          width: '100%',
          padding: '2px 0',
          zIndex: 1000,
        }}
        className="footer_area"
      >
        GC University Hyderabad, Kali Mori Hyderabad Sindh, Pakistan — Phone: 022-2111856
      </div>

    </>
  );
};

export default AdminPanel;
