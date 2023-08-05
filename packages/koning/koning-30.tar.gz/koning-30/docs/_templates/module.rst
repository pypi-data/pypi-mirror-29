.. title:: De gif toedieningen zijn de foltering !!


.. image:: jpg/bewijsgif4.jpg
    :width: 100%

{{ fullname }}
{{ underline }}

.. automodule:: {{ fullname }}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: Exceptions

   .. autosummary::
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

