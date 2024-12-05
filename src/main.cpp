#include "/Users/francescomarchisotti/Documents/Uni/Magistrale/Algoritmi/Libs/include/ode_solver.hpp"

#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>

using std::cerr;
using std::cin;
using std::cout;
using std::endl;

void RHS(const double &t, double Y[], double R[]);

int main() {
	std::ofstream out;
	out.open("data1.csv");
	if (!out) exit(1);

	const double tc   = 1 / 140.0;
	const double tmin = 0.0, tmax = 0.8 / tc;
	const int nStep = 1000;
	const double dt = (tmax - tmin) / nStep;
	double t        = tmin;

	const double theta0[] = {M_PI / 6, M_PI * 2.0 / 3.0};
	const double omega0   = 0.1;
	const double sigma    = 0.01;
	const double a        = 0.5;
	const double mu       = 1.0;
	double y[]            = {theta0[0], omega0, sigma, a, mu};
	const int nEq         = static_cast<int>(sizeof(y) / sizeof(y[0]));

	out << "t,theta,omega,sigma,a,mu" << endl;
	out << tc * t << "," << y[0] << "," << y[1] << "," << y[2] << "," << y[3]
		<< "," << y[4] << endl;
	for (int i = 0; i < nStep; i++) {
		rk4Step(t, y, RHS, dt, nEq);
		t += dt;

		if (y[0] >= M_PI) y[0] -= 2 * M_PI;

		out << tc * t << "," << y[0] << "," << y[1] << "," << y[2] << ","
			<< y[3] << "," << y[4] << endl;
	}

	out.close();

	out.open("data2.csv");
	if (!out) exit(1);

	double z[] = {theta0[1], omega0, sigma, a, mu};
	t          = tmin;

	out << "t,theta,omega,sigma,a,mu" << endl;
	out << tc * t << "," << z[0] << "," << z[1] << "," << z[2] << "," << z[3]
		<< "," << z[4] << endl;
	for (int i = 0; i < nStep; i++) {
		rk4Step(t, z, RHS, dt, nEq);
		t += dt;

		if (z[0] >= M_PI) z[0] -= 2 * M_PI;

		out << tc * t << "," << z[0] << "," << z[1] << "," << z[2] << ","
			<< z[3] << "," << z[4] << endl;
	}

	out.close();
	return 0;
}

void RHS(const double &t, double Y[], double R[]) {
	const double theta = Y[0];
	const double omega = Y[1];
	const double sigma = Y[2];
	const double a     = Y[3];
	const double mu    = Y[4];

	R[0] = omega;
	R[1] = (sigma + a * cos(t)) * sin(theta) - mu * omega;
	R[2] = 0.0;
	R[3] = 0.0;
	R[4] = 0.0;
}
