<template>
  <div class="page-home">
    <div class="top-crop">
      <img src="../assets/clinic.jpg" alt="" />
    </div>
    <div class="columns">
      <div class="column is-12">
        <section class="hero is-medium">
          <div class="hero-body">
            <div class="columns is-multiline">
              <div class="column is-three-fifths is-offset-one-fifth">
                <p class="is-size-3 has-text-link has-text-weight-semibold	">
                  Meet Our Doctors
                </p>
                <p class="subtitle">We care you</p>
              </div>
              <div class="column is-12">
                <div class="timeline is-centered">
                  <header class="timeline-header">
                    <span class="tag is-medium is-link">Sign up</span>
                  </header>
                  <div class="timeline-item is-info">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-info">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-info">
                    <div class="timeline-marker is-info is-icon">
                     <i class="fas fa-pen-alt"></i>
                    </div>
                    <div class="timeline-content">
                      <p class="heading">patient information</p>
                      <p>Fill out your information</p>
                    </div>
                  </div>
                  <div class="timeline-item is-primary">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-primary">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-primary">
                    <div class="timeline-marker is-primary is-icon">
                      <i class="fas fa-user-md"></i>
                    </div>
                    <div class="timeline-content">
                      <p class="heading">Doctors</p>
                      <p>Have a look at our doctors with experienced specialties</p>
                    </div>
                  </div>
                  <div class="timeline-item is-primary">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-success">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <div class="timeline-item is-success">
                    <div class="timeline-marker is-success is-icon">
                      <i class="fas fa-calendar-alt"></i>
                    </div>
                    <div class="timeline-content">
                      <p class="heading">Appointment</p>
                      <p>Select doctor, date, time with your symptom</p>
                    </div>
                  </div>
                  <div class="timeline-item is-success">
                    <div class="timeline-content">
                    </div>
                  </div>
                  <header class="timeline-header">
                    <span class="tag is-medium is-success">Visit us</span>
                  </header>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>

<style scoped>
.top-crop {
  max-height: 500px;
  overflow: hidden;
}
.top-crop img {
  margin: -380px 0 0;
}
</style>
