`{{ fullname }}`
=={{ underline }}

Source: :code:`{{ fullname.replace(".", "/") }}.py`

.. automodule:: {{ fullname }}
   :undoc-members:

   {% if name != "env" %}

   {% block functions %}
   {% if functions %}
   .. rubric:: Functions

   .. autosummary::
      :nosignatures:

   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}
   {% if classes %}
   .. rubric:: Classes

   .. autosummary::
      :toctree:
      :nosignatures:

   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: Exceptions

   .. autosummary::
      :nosignatures:

   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}


   {% block functionlist %}
   {% if functions %}
   {% for item in functions %}

   `{{ item }}`
   {{ "-" * (8 + item|length()) }}

   .. autofunction:: {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% endif %}
