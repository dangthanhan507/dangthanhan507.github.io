---
title: "CV"
permalink: /cv/
---

## Education

- Ph.D. in Robotics, University of Michigan, Ann Arbor, MI, January 2025–present
- M.S. in Robotics, University of Michigan, Ann Arbor, MI, December 2024
- B.S. in Computer Science, University of California, Irvine, CA, June 2023

## Work experience

<ul class="cv-experience">
  <li><strong>February 2026–present: Applied Scientist II Co-op</strong>
    <ul>
      <li>Amazon, North Reading, MA</li>
    </ul>
  </li>
  <li><strong>September 2023–present: Graduate Research Assistant</strong>
    <ul>
      <li>University of Michigan, Ann Arbor, MI</li>
      <li>Manipulation and Machine Intelligence Laboratory (<a href="https://www.mmintlab.com/">MMint</a>)</li>
      <li>Supervisor: <a href="https://www.mmintlab.com/people/nima-fazeli/">Nima Fazeli</a></li>
    </ul>
  </li>
  <li><strong>June 2023–August 2023: Autonomous Systems Software Intern</strong>
    <ul>
      <li>PassiveLogic, Salt Lake City, UT</li>
    </ul>
  </li>
  <li><strong>October 2022–December 2022: Embedded Software Engineering Intern</strong>
    <ul>
      <li>Persistent Systems LLC, New York City, NY</li>
      <li>Embedded C++ audio software</li>
    </ul>
  </li>
  <li><strong>September 2022–June 2023: Computer Vision Undergraduate Researcher</strong>
    <ul>
      <li>Computational Vision Lab, University of California, Irvine, CA</li>
      <li>Supervisor: Professor Fowlkes</li>
    </ul>
  </li>
  <li><strong>May 2022–August 2023: Undergraduate Researcher</strong>
    <ul>
      <li>EASEL Lab, University of California, Irvine, CA</li>
      <li>Supervisor: David Copp</li>
    </ul>
  </li>
</ul>

## Publications

{% assign publications = site.publications | sort: "order" | reverse %}
<ul class="cv-publications">
{% for item in publications %}
  <li>
    <h3><a href="{{ item.url | relative_url }}">{{ item.title }}</a></h3>
    <p>{{ item.authors | markdownify | remove: '<p>' | remove: '</p>' }}<br>
    {{ item.venue | default: item.status }}, {{ item.year }}</p>
  </li>
{% endfor %}
</ul>
