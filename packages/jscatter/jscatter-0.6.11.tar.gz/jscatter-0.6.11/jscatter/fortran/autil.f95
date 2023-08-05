!    -*- f90 -*-
! -*- coding: utf-8 -*-
! written by Ralf Biehl at the Forschungszentrum Juelich ,
! Juelich Center for Neutron Science 1 and Institute of Complex Systems 1
!    jscatter is a program to read, analyse and plot data
!    Copyright (C) 2018  Ralf Biehl
!
!    This program is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    This program is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with this program.  If not, see <http://www.gnu.org/licenses/>.
!

! f2py -c fscatter.f95 -m fscatter


module utils

    use typesandconstants

contains

function random_gauss(dim1,dim2)
    ! Gaussian random number with center 0 and 1-sigma =1 with shape of (dim1,dim2)
    ! uses Box-Muller transform
    use typesandconstants
    integer, intent(in) :: dim1,dim2
    real(dp), dimension(dim1,dim2) :: r, random_gauss

    CALL RANDOM_NUMBER(r)
    random_gauss(1:dim1:2,:) = SQRT(-2_dp*LOG(r(1:dim1:2,:))) * COS(2_dp*pi_dp*r(2:dim1:2,:))
    random_gauss(2:dim1:2,:) = SQRT(-2_dp*LOG(r(1:dim1:2,:))) * SIN(2_dp*pi_dp*r(2:dim1:2,:))
    
end function random_gauss

function interpolatesorted(x,y,fy)
    ! linear interpolation of sorted array
    ! if x is out of range the upper or lower boundary value is returned
    use typesandconstants
    real(dp),           intent(in)   :: x(:),y(:),fy(:)
    real(dp), dimension(size(x))    :: interpolatesorted
    integer                          :: i,j,imax ,jmax

    imax=size(x)
    jmax=size(y)
    do i =1,imax
        if  (x(i)<= y(1)) then
            interpolatesorted(i)=fy(1)
        else if  (x(i)>=y(jmax)) then
            interpolatesorted(i)=fy(jmax)
        else
            do j=1, jmax
                if  ( y(j)<=x(i) .and. x(i)<y(j+1) )    exit
            end do
            interpolatesorted(i)=interp1d_single(y(j),fy(j),y(j+1),fy(j+1),x(i))
        end if
    end do
end function interpolatesorted

function interp1d_single(x1,y1,x2,y2,xval)
    ! linear interpolation
    ! xval outside interval are linear extrapolated
    use typesandconstants
    real(dp),intent(in) :: x1,y1,x2,y2,xval
    real(dp) :: frac, interp1d_single
    frac = ( xval - x1 ) / ( x2 - x1 )
    interp1d_single = y1 + frac * ( y2 - y1 )
end function interp1d_single

function fibonaccilatticepointsonsphere(NN, r) result(lattice)
    ! create a Finonacci lattice with NN*2+1 points on sphere with radius r
    ! returns spherical coordinates r,theta, phi
    use typesandconstants
    integer,  intent(in)                :: NN
    real(dp), intent(in)                :: r

    real(dp), dimension(2*NN+1)         :: n
    integer                             :: i
    real(dp),dimension(2*NN+1,3)        :: lattice

    do i = 1,2*NN+1
        n(i)=(i-NN-1_dp)
    end do

    lattice(:,1)= r
    lattice(:,2)=  modulo((2*pi_dp * n / golden_dp) + pi_dp,  2*pi_dp) - pi_dp
    lattice(:,3)= asin(2_dp*n / (2 * NN + 1.)) + pi_dp / 2_dp

end function fibonaccilatticepointsonsphere

function rphitheta2xyz(rpt) result(xyz)
    ! transform rpt coordinates to cartesian
    use typesandconstants
    real(dp), intent(in)    :: rpt(:,:)
    real(dp),dimension(size(rpt,1),3) :: xyz

    xyz(:,1)=rpt(:,1)*cos(rpt(:,2))*sin(rpt(:,3))
    xyz(:,2)=rpt(:,1)*sin(rpt(:,2))*sin(rpt(:,3))
    xyz(:,3)=rpt(:,1)*cos(rpt(:,3))

end function rphitheta2xyz


end module utils
