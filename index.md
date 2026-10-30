---
title: "About me"
permalink: /
---

I am a PhD student in Robotics at the **University of Michigan, Ann Arbor**, and
an **Applied Scientist II Co-op at Amazon**. At Michigan, I work with Professor
**Nima Fazeli** in the **Manipulation and Machine Intelligence (MMint) Lab**.
My research focuses on **dexterous and contact-rich manipulation**. I started
my PhD in January 2025. I received my M.S. in Robotics from the
University of Michigan in December 2024 and my B.S. in
Computer Science from the University of California, Irvine in 2023.

You can reach me at [andang@umich.edu](mailto:andang@umich.edu).

## News

<ul class="news-list">
  <li>
    <time datetime="2026-04">April 2026</time>
    <span><a href="{{ '/publications/hydroshear/' | relative_url }}">HydroShear</a> was accepted to RSS 2026.</span>
  </li>
  <li>
    <time datetime="2026-02">February 2026</time>
    <span>I joined Amazon as an Applied Scientist II Co-op.</span>
  </li>
  <li>
    <time datetime="2026-01">January 2026</time>
    <span><a href="{{ '/publications/hydrosoft/' | relative_url }}">Hydrosoft</a> was accepted to ICRA 2026 in Vienna.</span>
  </li>
</ul>

## Selected research

{% assign selected = site.publications | where: "featured", true | sort: "order" | reverse %}
{% for item in selected %}
  {% include research-card.html item=item %}
{% endfor %}

[View all publications →]({{ '/publications/' | relative_url }})
