import React from 'react'
import colors from '../theme/Color'
import images from '../images/Image'

const SmallButton = ({
    btn_text, Color, backgroundColor, fontSize, src,
    fontWeight, imgwidth, imgheight, borderColor, justifyContent,
    textTransform, borderRadius, border, height, width, showbtnimg, onClick 
}) => {

    return (
        <>
            <div>
                <div style={{
                    // width: '90%',
                    display: 'flex',
                    // backgroundColor: 'blueviolet',
                    justifyContent: justifyContent ?? 'flex-end',

                }}>
                    <button className='btn_here'
                      onClick={onClick}
                        style={{
                            height: height ?? '12%',
                            width: width ?? 45,
                            // padding: '1% 1% 1% 1%',
                            cursor: 'pointer',
                            fontFamily: 'poppins',
                            fontWeight: fontWeight ?? '500',
                            letterSpacing: .2,
                            fontSize: fontSize ?? 7,
                            color: Color ?? colors.primary,
                            borderColor: borderColor,
                            borderRadius: borderRadius ?? 3,
                            textTransform: textTransform ?? 'capitalize',
                            backgroundColor: backgroundColor ?? colors.success,
                            border: 'none',

                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',

                        }}>
                        <div style={{ fontFamily: 'poppins' }}>
                            {btn_text}
                        </div>

                        {showbtnimg == false ? '' :
                            <div style={{ display: 'flex', alignItems: 'baseline', alignItems: 'center', position: 'relative', left: 2 }}>
                                <img src={src ?? images.editicon} alt='icon'
                                    height={imgheight ?? 8}
                                    width={imgwidth ?? 8}
                                    style={{ backgroundPosition: 'center', backgroundSize: 'cover', }}
                                />
                            </div>
                        }
                    </button>
                </div>
            </div>
        </>
    )
}

export default SmallButton