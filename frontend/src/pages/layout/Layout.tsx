import {Outlet, NavLink, Link} from "react-router-dom";

import styles from "./Layout.module.css";

const Layout = () => {
    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitle}>Home</h3>
                    </Link>
                    <nav>
                        <ul className={styles.headerNavList}>
                            <li className={styles.headerNavLeftMargin}>
                                <NavLink to="/checklist" className={styles.headerNavPageLink}>Checklists</NavLink>
                            </li>
                        </ul>
                    </nav>
                </div>
            </header>

            <Outlet/>
        </div>
    );
};

export default Layout;