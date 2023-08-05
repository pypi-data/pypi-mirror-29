function basegauge(widget_id, url, skin, parameters)
{
    // Will be using "self" throughout for the various flavors of "this"
    // so for consistency ...
    
    self = this
    
    // Initialization
    
    self.widget_id = widget_id
    
    // Store on brightness or fallback to a default
        
    // Parameters may come in useful later on
    
    self.parameters = parameters
       
    var callbacks = []

    // Define callbacks for entities - this model allows a widget to monitor multiple entities if needed
    // Initial will be called when the dashboard loads and state has been gathered for the entity
    // Update will be called every time an update occurs for that entity
     
    self.OnStateAvailable = OnStateAvailable
    self.OnStateUpdate = OnStateUpdate
    
    if ("entity" in parameters)
    {
        var monitored_entities = 
            [
                {"entity": parameters.entity, "initial": self.OnStateAvailable, "update": self.OnStateUpdate}
            ]
    }
    else
    {
        var monitored_entities =  []
    }

    self.gauge = new JustGage({
    parentNode: $('#' + widget_id + ' > div')[0],
    //id: "graph",
    value: 0,
    nogradient: true,
    levelColors: [self.parameters.low_color, self.parameters.med_color, self.parameters.high_color],
    labelFontColor: self.parameters.color,
    valueFontColor: self.parameters.color,
    levelColorsGradient: false,
    gaugeColor: self.parameters.bgcolor,
    symbol: self.parameters.units,
    min: self.parameters.min,
    max: self.parameters.max,
  });


    // Finally, call the parent constructor to get things moving
    
    WidgetBase.call(self, widget_id, url, skin, parameters, monitored_entities, callbacks)  

    // Function Definitions
    
    // The StateAvailable function will be called when 
    // self.state[<entity>] has valid information for the requested entity
    // state is the initial state
    // Methods

    function OnStateAvailable(self, state)
    {    
        set_value(self, state)
    }
 
    function OnStateUpdate(self, state)
    {
        set_value(self, state)
    }

    function set_value(self, state)
    {
        self.gauge.refresh(state.state)
    }
}