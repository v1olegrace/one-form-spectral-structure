"""Independent checks for the expanded spectral manuscript.

No experimental data. Exact symbolic checks, multiprecision quadratures with
two substitutions, sampled moment pencils, and synthetic error envelopes.
Floating-point agreement is not a rigorous interval quadrature certificate.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['svg.hashsalt'] = 'physics-of-all'
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
import sympy as sy

from analysis import dirac_moment, save_svg
from laplace_geometry import scaled_moment, Gamma
from moment_conditions import mass_from_log_ratio, moment_gate

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'output/data'
FIG = ROOT / 'output/figures'
CHECKS = []


def check(name, condition, detail=None):
    ok = bool(condition)
    CHECKS.append({'name': name, 'passed': ok, 'detail': detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name}", flush=True)


def pencil(b, K):
    """Sampled Hausdorff pencil (C_1, C_0) in y = e^{-hx}.

    The shared finite necessary conditions run on the 2K+2 samples this pencil
    actually consumes, so an unresolved pencil is refused rather than divided
    by.  The largest eigenvalue is returned; it is an average of y over a
    positive measure and must be handed to ``mass_from_log_ratio``.
    """
    a = list(b[:2*K+2])
    if len(a) != 2*K+2:
        raise ValueError("pencil requires exactly 2K+2 samples")
    ok, reason, diag = moment_gate(a, strict_shift=0)
    if not ok:
        raise ValueError(f"No bound: {reason}")
    c0 = mp.matrix([[a[i+j] for j in range(K+1)] for i in range(K+1)])
    c1 = mp.matrix([[a[i+j+1] for j in range(K+1)] for i in range(K+1)])
    inv = mp.inverse(mp.cholesky(c0))
    s = inv*c1*inv.T
    eigenvalues, eigenvectors = mp.eigsy((s+s.T)/2)
    index = K
    return eigenvalues[index], inv.T*eigenvectors[:, index], c0, c1, diag


def _optional_mass(ratio, h, what):
    """Return the mass bound, or None when the domain guard refuses the ratio."""
    try:
        return mass_from_log_ratio(ratio, h, what=what)
    except ValueError:
        return None


def symbolic_checks():
    t, m = sy.symbols('t m', positive=True)
    x = 2*m+t
    shape = (x*x+2*m*m)/x**2*sy.sqrt(x*x-4*m*m)/(3*sy.sqrt(m*t))
    series = sy.series(shape, t, 0, 3).removeO().expand()
    expected = 1-5*t/(24*m)+77*t*t/(384*m*m)
    check('Exact Dirac edge density coefficients', sy.simplify(series-expected)==0)
    p, beta, gamma = sy.Rational(3,2), -sy.Rational(5,24)/m, sy.Rational(77,384)/m**2
    cubic = sy.simplify(2*gamma*p*(p+1)-(beta*p)**2)
    check('Exact cubic edge coefficient 45/(32 m^2)', cubic==sy.Rational(45,32)/m**2)
    z, g, A = sy.symbols('z g A')
    expansion = sy.series(g**2/(1-g**2*A), g, 0, 6).removeO()
    check('Dyson sign: positive spectral correction', sy.expand(expansion).coeff(g,4)==A)
    P = sy.diag(1, 0)
    S = sy.Matrix([[0,1],[1,0]])
    T = (S-sy.eye(2))/sy.I
    psi = sy.Matrix([1,2])/sy.sqrt(5)
    lhs = sy.simplify(2*sy.im((psi.conjugate().T*P*T*psi)[0]))
    rhs = (psi.conjugate().T*(T.conjugate().T*P*T-S.conjugate().T*P*S+P)*psi)[0]
    check('Exact broken-projector identity and -2/5 counterexample', lhs==-sy.Rational(2,5) and sy.simplify(lhs-rhs)==0)
    sector = sy.Matrix([1,0])
    check('Sector-pure state retains nonnegative left side', sy.simplify(2*sy.im((sector.T*P*T*sector)[0]))==2)
    r = sy.symbols('r', positive=True)
    bad = sy.exp(-r)-sy.exp(-2*r)/2
    check('Screening alone does not imply complete monotonicity', sy.diff(bad,r,2).subs(r,sy.log(2)/2)<0)
    return {'dirac_density_series': str(series), 'cubic_coefficient': str(cubic)}


def independent_gamma(r):
    """x=2cosh(u), a different substitution from the production integrator."""
    def integrand(u, n):
        x = 2*mp.cosh(u)
        density = (x+2/x)*mp.tanh(u)/(6*mp.pi**2)
        return x**n*mp.exp(-r*(x-2))*density*2*mp.sinh(u)
    # Endpoint u=8 has exponent below -2900 even for r=0.5.
    return mp.quad(lambda u: integrand(u,1), [0,.25,1,2,4,8])/mp.quad(
        lambda u: integrand(u,0), [0,.25,1,2,4,8])


def quadrature_checks():
    rows=[]
    for rs in ['0.5','1','3','10','40','80']:
        r=mp.mpf(rs)
        a=Gamma(r)
        b=independent_gamma(r)
        error=abs(a-b)
        check(f'Independent quadrature variables r={rs}', error<mp.mpf('1e-35'), mp.nstr(error,5))
        rows.append({'r':rs,'Gamma':mp.nstr(a,22),'absolute_difference':mp.nstr(error,6)})
    return rows


def sampled_checks():
    rows=[]
    robust=[]
    for rs,hs in [('1','0.5'),('3','0.5'),('1','1')]:
        r,h=mp.mpf(rs),mp.mpf(hs)
        base=scaled_moment(0,r)
        b=[mp.exp(-2*j*h)*scaled_moment(0,r+j*h)/base for j in range(12)]
        previous=mp.inf
        for K in range(6):
            L,v,c0,c1,diag=pencil(b,K)
            bound=mass_from_log_ratio(L,h,what=f'sampled pencil eigenvalue K={K}')
            check(f'Finite moment conditions on the samples r={rs} h={hs} K={K}',
                  diag['status']=='CHECKED_COMPATIBLE', diag['status'])
            check(f'Sampled bound and nested spaces r={rs} h={hs} K={K}',
                  bound>=2-mp.mpf('1e-40') and bound<=previous+mp.mpf('1e-40'))
            if K==0:
                check(f'Two-radius sandwich r={rs} h={hs}', Gamma(r+h)<=bound<=Gamma(r))
            previous=bound
            rows.append({'r':rs,'h':hs,'K':K,'samples':2*K+2,
                         'bound':float(bound),'excess_percent':float((bound/2-1)*100),
                         'bound_25_digits':mp.nstr(bound,25)})
            if rs=='1' and hs=='0.5':
                for frac in ['0.000001','0.005']:
                    eps=[mp.mpf(frac)*bj for bj in b]
                    e=[sum(abs(v[i]*v[j])*eps[i+j+a] for i in range(K+1) for j in range(K+1)) for a in range(2)]
                    numerator=(v.T*c1*v)[0]-e[1]
                    denominator=(v.T*c0*v)[0]+e[0]
                    lower=numerator/denominator if numerator>0 and denominator>0 else None
                    safe=(_optional_mass(lower,h,f'robust envelope ratio K={K}')
                          if lower is not None else None)
                    check(f'Robust envelope or explicit no-bound eps={frac} K={K}',
                          safe is None or (safe>=bound and safe>=2))
                    robust.append({'K':K,'relative_absolute_envelope':frac,
                                   'nominal':float(bound),'robust':float(safe) if safe is not None else None,
                                   'status':'finite' if safe is not None else 'refused_no_valid_ratio'})
    # Exact finite support: the K=1 pencil resolves two atoms.
    h=mp.mpf('0.4')
    masses=[mp.mpf('0.7'),mp.mpf('2.3')]
    b=[mp.mpf('.02')*mp.exp(-h*masses[0]*j)+mp.mpf('.98')*mp.exp(-h*masses[1]*j) for j in range(4)]
    L,_,_,_,_=pencil(b,1)
    check('Two-atom finite-rank recovery K=1',
          abs(mass_from_log_ratio(L,h,what='two-atom pencil')-masses[0])<mp.mpf('1e-40'))
    return rows,robust


def mellin_checks():
    """Nested real quadrature, not reuse of the beta formula being checked."""
    def phi_scipy(r):
        def integrand(y):
            x=2+y*y/r
            rho=(1+2/x**2)*math.sqrt(max(0,1-4/x**2))/(12*math.pi**2)
            return 4*y*x/r*rho*math.exp(-y*y)
        scaled=quad(integrand,0,10,epsabs=1e-12,epsrel=1e-11)[0]
        return math.exp(-2*r)*scaled
    rows=[]
    for n in [1,2,3]:
        radial,err=quad(lambda r:r**(2*n+1)*phi_scipy(r),0,np.inf,epsabs=1e-11,epsrel=1e-10)
        recovered=radial/math.gamma(2*n+2)
        expected=dirac_moment(n)
        relative=abs(recovered/expected-1)
        check(f'Independent nested radial Mellin integral n={n}',relative<2e-8,relative)
        rows.append({'n':n,'from_radial_profile':recovered,'beta_formula':expected,
                     'relative_difference':relative,'outer_quad_error_estimate':err})
    return rows


def hidden_checks():
    M,mu,eps,T=2.0,0.4,1e-8,3.0
    t=np.linspace(0,T,1001)
    f0=np.exp(-M*t)
    fe=(1-eps)*f0+eps*np.exp(-mu*t)
    check('Hidden atom absolute error envelope', np.max(abs(fe-f0))<=eps)
    check('Hidden atom relative window formula', abs(np.max((fe-f0)/f0)-eps*np.expm1((M-mu)*T))<1e-14)
    # Atom plus same-edge flat continuum: Phi=e^-Mr (Z+C/r).
    r=mp.mpf(1000)
    Z,C=mp.mpf(2),mp.mpf(3)
    gamma=2+(C/r**2)/(Z+C/r)
    check('Atom touching continuum has algebraic correction', abs(r*r*(gamma-2)-C/Z)<mp.mpf('.003'))
    return {'M':M,'mu':mu,'epsilon':eps,'T':T,
            'max_relative_window_error':float(eps*np.expm1((M-mu)*T)),
            'crossover':float(np.log((1-eps)/eps)/(M-mu))}


def write_outputs(results):
    DATA.mkdir(parents=True,exist_ok=True)
    FIG.mkdir(parents=True,exist_ok=True)
    for name,rows in [('sampled_hierarchy',results['sampled']),('robust_sampled_bounds',results['robust'])]:
        with (DATA/f'{name}.csv').open('w',newline='',encoding='utf-8') as stream:
            writer=csv.DictWriter(stream,fieldnames=rows[0].keys())
            writer.writeheader();writer.writerows(rows)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(7.2,4.1),layout='constrained')
    for r,h in [('1','0.5'),('3','0.5'),('1','1')]:
        rows=[v for v in results['sampled'] if v['r']==r and v['h']==h]
        ax.plot([v['K'] for v in rows],[v['bound'] for v in rows],'o-',label=f'r={r}, h={h}')
    ax.axhline(2,color='#8b2f3f',linestyle='--',label='Limiar do benchmark: 2')
    ax.set(xlabel='Ordem K',ylabel='Limite superior para M* (m=1)',xticks=range(6))
    ax.legend();ax.grid(alpha=.15)
    fig.savefig(FIG/'sampled_hierarchy.png',dpi=200);save_svg(fig,FIG/'sampled_hierarchy.svg');plt.close(fig)
    t=np.linspace(0,20,600)
    hidden=results['hidden']
    fig,ax=plt.subplots(figsize=(7.2,4.1),layout='constrained')
    for eps in [1e-2,1e-5,1e-8]:
        light=eps*np.exp((hidden['M']-hidden['mu'])*t)/(1-eps)
        gamma=(hidden['M']+hidden['mu']*light)/(1+light)
        ax.plot(t,gamma,label=f'Peso leve = {eps:g}')
    ax.axhline(hidden['mu'],color='#8b2f3f',linestyle='--',label='Borda verdadeira = 0,4')
    ax.set(xlabel='Raio após normalização t',ylabel='Derivada logarítmica do perfil')
    ax.legend();ax.grid(alpha=.15)
    fig.savefig(FIG/'hidden_threshold.png',dpi=200);save_svg(fig,FIG/'hidden_threshold.svg');plt.close(fig)
    lines=['### Hierarquia de amostras: dados sem ruído\n',
           '| $r$ | $h$ | $K$ | Amostras | Limite $\\mathcal B_K$ | Excesso |',
           '|---:|---:|---:|---:|---:|---:|']
    for row in results['sampled']:
        if row['h']=='0.5':
            lines.append(f"| {row['r']} | {row['h']} | {row['K']} | {row['samples']} | {row['bound']:.8f} | {row['excess_percent']:.3f}% |")
    lines+=['\n### Efeito do orçamento de erro\n',
            'Amostras centrais iguais ao benchmark, com envelopes absolutos simultâneos de 0,5% de cada valor central; não se trata de cobertura estatística de dados experimentais. A coluna robusta usa o vetor do feixe nominal e a equação (24), sem afirmar otimização global.\n',
            '| $K$ | Limite nominal | Limite robusto |','|---:|---:|---:|']
    for row in results['robust']:
        if row['relative_absolute_envelope']=='0.005':
            safe=f"{row['robust']:.8f}" if row['robust'] is not None else 'Sem numerador positivo'
            lines.append(f"| {row['K']} | {row['nominal']:.8f} | {safe} |")
    lap=json.loads((DATA/'laplace_geometry_certification.json').read_text())
    lines+=['\n### Expansão de borda recalculada\n',
            '| $r$ | $\\Gamma(r)$ | $r[\\Gamma-2]$ | $r^3[\\Gamma-2-3/(2r)+5/(16r^2)]$ |',
            '|---:|---:|---:|---:|']
    for row in lap['theorem_D_edge_law']['table']:
        lines.append(f"| {row['r']} | {row['Gamma']} | {row['r_times_Gamma_minus_2m']} | {row['scaled_cubic_residual']} |")
    lines+=['\nA última coluna deve convergir a $45/32=1{,}40625$. O teste compara 60 e 90 dígitos; o teste independente adicional usa $x=2\\cosh u$. O cálculo anterior em $r=80$, sem extração do exponencial comum, não reproduzia esses dígitos apesar de passar o teste assintótico mais permissivo.\n',
            '### Identidade de Mellin: quadratura radial independente\n',
            '| $n$ | $c_n$ pelo perfil radial | Erro relativo à fórmula beta |','|---:|---:|---:|']
    for row in results['mellin']:
        lines.append(f"| {row['n']} | {row['from_radial_profile']:.12g} | {row['relative_difference']:.3g} |")
    (ROOT/'manuscript/numerical_results.qmd').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    results['checks']=CHECKS
    results['all_checks_passed']=all(v['passed'] for v in CHECKS)
    results['check_count']=len(CHECKS)
    results['environment']={'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
                            'mpmath':mp.__version__,'sympy':sy.__version__,'matplotlib':matplotlib.__version__}
    results['scope']='Synthetic model checks; floating-point quadrature, not interval certification or experimental validation.'
    (DATA/'extended_verification.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    mp.mp.dps=60
    results={'symbolic':symbolic_checks(),'quadrature':quadrature_checks()}
    results['sampled'],results['robust']=sampled_checks()
    results['mellin']=mellin_checks()
    results['hidden']=hidden_checks()
    write_outputs(results)
    print(f"{len(CHECKS)} checks; all passed: {results['all_checks_passed']}")
    if not results['all_checks_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
