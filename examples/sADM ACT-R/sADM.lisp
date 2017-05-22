(clear-all)

(define-model json-test

  (sgp :jni-hostname "localhost" :jni-port 5555 :jni-sync t)

  (chunk-type (vis-stim (:include visual-object)))
  (chunk-type goal-state state)
  

  ; (add-dm
  ;  (o-blue isa color-opposite color blue opposite red)
  ;  (o-red isa color-opposite color red opposite blue)
  ;  (d-white isa search-direction color white direction counter-clockwise)
  ;  (d-back isa search-direction color black direction clockwise)
  ;  (quad1 isa quad quad 1 clockwise 2 counter-clockwise 4)
  ;  (quad2 isa quad quad 2 clockwise 3 counter-clockwise 1)
  ;  (quad3 isa quad quad 3 clockwise 4 counter-clockwise 2)
  ;  (quad4 isa quad quad 4 clockwise 1 counter-clockwise 3)
  
  
  ;  object1 isa object object nil shape nil size nil pitch nil instrument nil tempo nil texture nil material nil consistency nil points nil deadline nil queuenum nil priority nil)

  (sgp :v t)
  ;(sgp :needs-mouse nil :process-cursor t)
  ;(start-hand-at-mouse)

  (p find-stim
     ?goal>
      buffer empty
     =visual-location>
      isa visual-location
     ==>
     +visual-location>
      isa visual-location
   )

  (p attend-stim
     ?goal>
      buffer empty
     =visual-location>
      isa visual-location
     ?manual>
      preparation free
     ?visual>
      state free
     ==>
     +goal>
      isa goal-state
      state found-stim
     +visual>
      cmd move-attention
      screen-pos =visual-location
   )


   (p encode-stim
      =goal>
       state found-stim
      =visual>
       value =letter
      ?manual>
       state free
      ==>
      -goal>
      +manual>
       cmd press-key
       key =letter
    )

  )
