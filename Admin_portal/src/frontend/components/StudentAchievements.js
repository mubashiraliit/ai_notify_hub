import React, { useState, useEffect } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import SmallButton from '../../components/SmallButton';
import HeadingHere from '../../components/HeadingHere';

const StudentAchievements = () => {
  const [achievements, setAchievements] = useState([]);
  const [newAchievement, setNewAchievement] = useState('');

  // ✅ Fetch all achievements
  const fetchAchievements = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/achievements');
      setAchievements(res.data || []);
    } catch (err) {
      console.error('Fetch error:', err);
      alert('Failed to fetch achievements.');
    }
  };

  useEffect(() => {
    fetchAchievements();
  }, []);

  // ✅ Add new achievement
  const handleAdd = async () => {
    if (!newAchievement.trim()) return alert('Please enter an achievement.');
    try {
      const res = await axios.post('http://localhost:5000/api/achievements', {
        achievement: newAchievement.trim(),
      });
      alert(res.data?.message || 'Achievement added successfully.');
      setNewAchievement('');
      fetchAchievements();
    } catch (err) {
      alert(err.response?.data?.message || 'Add failed.');
    }
  };

  // ✅ Update specific achievement
  const handleUpdate = async (id, text) => {
    if (!text.trim()) return alert('Achievement text cannot be empty.');
    try {
      const res = await axios.put(`http://localhost:5000/api/achievements/${id}`, {
        achievement: text.trim(),
      });
      alert(res.data?.message || 'Achievement updated successfully.');
      fetchAchievements();
    } catch (err) {
      alert(err.response?.data?.message || 'Update failed.');
    }
  };

  // ✅ Delete specific achievement
  const handleDelete = async (id) => {
    try {
      const res = await axios.delete(`http://localhost:5000/api/achievements/${id}`);
      alert(res.data?.message || 'Achievement deleted successfully.');
      fetchAchievements();
    } catch (err) {
      alert(err.response?.data?.message || 'Delete failed.');
    }
  };

  // ✅ Delete all achievements
  const handleDeleteAll = async () => {
    if (!window.confirm('Delete all achievements?')) return;
    try {
      const res = await axios.delete('http://localhost:5000/api/achievements/');
      alert(res.data?.message || 'All achievements deleted successfully.');
      fetchAchievements();
    } catch (err) {
      alert(err.response?.data?.message || 'Delete all failed.');
    }
  };

  return (
    <div className="sub_third_area" style={{ backgroundColor: colors.light_grey }}>
      <div className="row_head_area">
        <HeadingHere text={'students achievements'} ShowLine={true} fontSize={12} width={'50%'} />

        <div style={{ display: 'flex', gap: 6 }}>
          {/* <SmallButton
            btn_text="add"
            fontSize={9}
            width={50}
            justifyContent="center"
            backgroundColor={colors.success}
            showbtnimg={false}
            onClick={handleAdd}
          /> */}
          {/* <SmallButton

            btn_text="delete all"
            fontSize={9}
            width={60}
            justifyContent="center"
            backgroundColor={colors.secondary}
            showbtnimg={false}
            onClick={handleDeleteAll}
          /> */}
        </div>
      </div>

      {/* ✅ New Achievement Input */}
      {/* <input
        type="text"
        placeholder="Enter new achievement..."
        value={newAchievement}
        onChange={(e) => setNewAchievement(e.target.value)}
        maxLength={100}
        className="mid_term_inpt"
        style={{
          outline: 'none',
          border: `1px solid ${colors.success}`,
          width: '90%',
          marginLeft: '1.5%',
          borderRadius: 6,
          marginTop: 8,
          marginBottom: 12,
        }}

      /> */}

      {/* ✅ Achievements List */}
      <div className="point_hightlight_area" style={{ marginTop: '3%' }}>
        {achievements.map((a, i) => (
          <div key={a._id} style={{ marginBottom: "2%",width:'100%' }}>

            <textarea
              className="point_hightlight"
              style={{ color: colors.black,fontSize:11, outline: 'none', border: `1px solid ${colors.success}`, 
              resize: 'none', backgroundColor: 'transparent', }}  maxLength={100}
              value={a.achievement}
              row={2}
              onChange={(e) => {
                const copy = [...achievements];
                copy[i].achievement = e.target.value;
                setAchievements(copy);
              }}

            // style={{
            //   color: colors.black,
            //   outline: 'none',
            //   border: `1px solid ${colors.success}`,
            //   backgroundColor: 'transparent',
            //   width: '98%',
            //   margin: '0 auto',
            //   display: 'block',
            //   borderRadius: 6,
            //   padding: '6px 8px',
            //   resize: 'none',
            // }}
            />
            <>

              
            <div style={{ display: 'flex', gap: 6, marginTop: 3 }}>
            <SmallButton
            btn_text="update"
            fontSize={9}
            width={50}
            justifyContent="center"
            backgroundColor={colors.secondary}
            showbtnimg={false}
            onClick={() => handleUpdate(a._id, a.achievement)}
            />
            {/* <SmallButton
            btn_text="delete"
            fontSize={9}
            width={50}
            justifyContent="center"
            backgroundColor={colors.danger}
            showbtnimg={false}
            onClick={() => handleDelete(a._id)}
            /> */}
            </div>
            </>
          </div>
        ))}

        {/* <textarea className='point_hightlight' type='text' style={{ color: colors.black, outline: 'none', border: `1px solid ${colors.success}`, resize: 'none', backgroundColor: 'transparent', }}
          defaultValue={"CS students won 1st place in National Coding Hackathon 2025."} maxLength={100} />
        <textarea className='point_hightlight' type='text' style={{ color: colors.black, outline: 'none', border: `1px solid ${colors.success}`, resize: 'none', backgroundColor: 'transparent', }}
          defaultValue={"Business team earned PKR 500k HEC Startup Pakistan grant."} maxLength={100} />
        <textarea className='point_hightlight' type='text' style={{ color: colors.black, outline: 'none', border: `1px solid ${colors.success}`, resize: 'none', backgroundColor: 'transparent', }}
          defaultValue={"Computer Science students selected for Erasmus Exchange Program in Turkey."} maxLength={100} />
        <textarea className='point_hightlight' type='text' style={{ color: colors.black, outline: 'none', border: `1px solid ${colors.success}`, resize: 'none', backgroundColor: 'transparent', }}
          defaultValue={"GCUH Cricket Team won Inter-Collegiate Championship Trophy 2025."} maxLength={100} /> */}

      </div>
    </div>
  );
};

export default StudentAchievements;
