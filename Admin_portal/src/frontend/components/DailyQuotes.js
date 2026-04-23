import React, { useState, useEffect } from 'react';
import axios from 'axios';
import colors from '../../theme/Color';
import SmallButton from '../../components/SmallButton';
import HeadingHere from '../../components/HeadingHere';

const DailyQuotes = () => {
  const [quoteText, setQuoteText] = useState('');
  const [quoteId, setQuoteId] = useState(null);

  // ✅ Fetch quote
  const fetchQuote = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/quotes');
      const data = res.data;
      if (data && data.quotes) {
        setQuoteText(data.quotes);
        setQuoteId(data._id || null);
      } else {
        setQuoteText('');
        setQuoteId(null);
      }
    } catch (err) {
      console.error('Fetch error:', err);
      alert('Failed to fetch daily quote.');
    }
  };

  useEffect(() => {
    fetchQuote();
  }, []);

  // ✅ Add quote
  const handleAdd = async () => {
    if (!quoteText.trim()) return alert('Please enter a quote.');
    try {
      const res = await axios.post('http://localhost:5000/api/quotes/create', {
        quotes: quoteText,
      });
      alert(res.data?.message || 'Quote added successfully.');
      fetchQuote();
    } catch (err) {
      console.error('Add error:', err);
      alert(err.response?.data?.message || 'Add failed.');
    }
  };

  // ✅ Update quote
  const handleUpdate = async () => {
    if (!quoteId) return alert('No quote found to update.');
    try {
      const res = await axios.put(`http://localhost:5000/api/quotes/${quoteId}`, {
        quotes: quoteText,
      });
      alert(res.data?.message || 'Quote updated successfully.');
      fetchQuote();
    } catch (err) {
      console.error('Update error:', err);
      alert(err.response?.data?.message || 'Update failed.');
    }
  };

  // ✅ Delete quote
  const handleDelete = async () => {
    if (!quoteId) return alert('No quote found to delete.');
    try {
      const res = await axios.delete(`http://localhost:5000/api/quotes/${quoteId}`);
      alert(res.data?.message || 'Quote deleted successfully.');
      fetchQuote();
    } catch (err) {
      console.error('Delete error:', err);
      alert(err.response?.data?.message || 'Delete failed.');
    }
  };

  return (
    <div
      className="headeing_qoute_area"
      style={{ backgroundColor: colors.light_grey }}
    >
      <div className="row_head_area">
        <HeadingHere text={'Daily Quotes :'} fontSize={17} />
        <div style={{ display: 'flex', gap: 6 }}>
          {/* <SmallButton
            btn_text="add"
            fontSize={9}
            width={45}
            justifyContent={'center'}
            backgroundColor={colors.success}
            showbtnimg={false}
            onClick={handleAdd}
          /> */}
          <SmallButton
            btn_text="update"
            fontSize={9}
            width={55}
            justifyContent={'center'}
            backgroundColor={colors.success}
            showbtnimg={false}
            onClick={handleUpdate}
          />
          {/* <SmallButton
            btn_text="delete"
            fontSize={9}
            width={55}
            justifyContent={'center'}
            backgroundColor={colors.danger}
            showbtnimg={false}
            onClick={handleDelete}
          /> */} 
        </div>
      </div>

      <input
        className="inpt_hightlight"
        type="text"
        style={{ color: colors.secondary,fontSize:14, outline: 'none' }}
        value={quoteText}
        onChange={(e) => setQuoteText(e.target.value)}
        maxLength={70}
      />
    </div>
  );
};

export default DailyQuotes;
