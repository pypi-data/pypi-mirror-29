      program test
!
      implicit none
      integer i, j, n, m
      double precision a, b
!
      n = 10000
      m = 100
      a = 1.d0
!
      open(10, file="output", status="unknown")
      open(20, file="input" , status="unknown")
      read(20,*) b
      close(20)
!
      do i = 1, n
        if (mod(i,m) .eq. 0) then
           write(10,*) "outer loop:",i
           call flush(10)
        end if
        do j = 1, n
          a = (a + b)/a 
        end do
      end do
!
      write(10,*)
      write(10,*) 'result : ',a

      close(10)
!
      end program
