{{ fullname }}
{{ underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
   :members:
   :undoc-members:
   :private-members:
   :show-inheritance:
   :special-members:

   ..
      Comment out the autosummary blocks until Sphinx PR #4029 is merged.

   {% block methods %}
   {% if methods %}
   ..
      .. rubric:: Methods

      .. autosummary::
      {% for item in methods %}
         ~{{ name }}.{{ item }}
      {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   ..
      .. rubric:: Attributes

      .. autosummary::
      {% for item in attributes %}
         ~{{ name }}.{{ item }}
      {%- endfor %}
   {% endif %}
   {% endblock %}
