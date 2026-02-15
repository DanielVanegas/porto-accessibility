def build_query(mode):
    if mode in ["WALK", "BICYCLE"]:
        modes_block = f"""
        modes: {{
          directOnly: true
          direct: [{mode}]
        }}
        preferences: {{
          street: {{
            walk: {{
              speed: 1.2
              reluctance: 2.0
            }}
            bicycle: {{
              speed: 4.5
              reluctance: 1.0
              optimization: {{
                type: FLAT_STREETS
              }}
            }}
          }}
        }}
        """
    elif mode == "TRANSIT":
        modes_block = """
        modes: {
          transitOnly: true
          transit: {
            access: [WALK]
            egress: [WALK]
            transfer: [WALK]
            transit: [
              { mode: BUS }
            ]
          }
        }
        preferences: {
          street: {
            walk: {
              speed: 1.2
              reluctance: 10.0
            }
          }
        }
        """
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    query = f"""
    query($fromLat: CoordinateValue!, $fromLon: CoordinateValue!, $toLat: CoordinateValue!, $toLon: CoordinateValue!, $dateTime: OffsetDateTime!) {{
      planConnection(
        dateTime: {{ earliestDeparture: $dateTime }}
        first: 1
        origin: {{
          location: {{ coordinate: {{ latitude: $fromLat, longitude: $fromLon }} }}
          label: "Origin"
        }}
        destination: {{
          location: {{ coordinate: {{ latitude: $toLat, longitude: $toLon }} }}
          label: "Destination"
        }}
        {modes_block}
      ) {{
        edges {{
          node {{
            start
            end
            walkDistance
            walkTime
            legs {{
              mode
              distance
              start {{
                scheduledTime
              }}
              end {{
                scheduledTime
              }}
            }}
          }}
        }}
      }}
    }}
    """
    return query
