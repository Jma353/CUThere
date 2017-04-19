import React from 'react';
require('../../../public/sass/VenueDetail.scss');

/**
 * Displays abbreviated information about a venue (meant to
 * be used when displaying recommended venues after searching)
 */
class VenueDetail extends React.Component {

  /**
   * Render
   */
  render () {
    return (
      <div className='venue-detail-container'>
        {/* Image */}
        <div className='venue-detail-img'>
          <img src={this.props.data.profile_picture} />
        </div>
        <div className='venue-detail-text-container'>
          {/* Title */}
          <div className='venue-detail-title'>
            {this.props.data.name}
          </div>
          {/* Address */}
          <div className='venue-detail-address'>
            <p>{this.props.data.street}</p>
            <p>{this.props.data.city}, {this.props.data.state} {this.props.data.zip}</p>
          </div>
          {/* Description */}
          <div className='venue-detail-description'>
            {this.props.data.about}
          </div>
        </div>
      </div>
    );
  }
}

export default VenueDetail;
