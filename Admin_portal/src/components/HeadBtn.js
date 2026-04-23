import React from 'react'
import colors from '../theme/Color'
import SmallButton from './SmallButton'

const HeadBtn = ({ text, textTransform, fontSize, fontWeight, width, 
    // show, backgroundColor, borderColor, border 
}) => {
    return (
        <>
            <div className='head_text_area'
                style={{
                    fontFamily: 'poppins',
                    padding: '1% 2%',
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                }}
            >
                <div className='head_btn_area'>
                    <div className='head_text'
                        style={{
                            color: colors.secondary,
                            fontSize: fontSize ?? 16,
                            textTransform: textTransform ?? 'capitalize',
                            fontWeight: fontWeight ?? 700
                        }}
                    >
                        {text}
                    </div>

                    <div className='head_area_line'
                        style={{
                            position: 'relative',
                            height: 3,
                            width: width ?? '10%',
                            marginTop: 3,
                            backgroundColor: colors.success
                        }}
                    ></div>
                </div>
                <div>
                    {/* {show ? <SmallButton btn_text={'update'} fontSize={9.5}
                        fontWeight={500} imgwidth={11} imgheight={11}
                        backgroundColor={backgroundColor ?? colors.secondary}
                        borderColor={borderColor} border={border}
                    /> : ''} */}
                </div>
            </div>
        </>
    )
}

export default HeadBtn